#!/usr/bin/env bash
# Stand up the profile cluster, drain a worker and power it off the way Wattproof
# would, check the service survived it, and print the README block on stdout.
set -euo pipefail
cd "$(dirname "$0")/.."

off=profile-worker3

trap 'kind delete cluster --name profile >&2' EXIT
kind create cluster --config k8s/kind.yaml --wait 120s >&2
# --wait only covers the control plane. A worker still joining carries the
# not-ready taint, and with nodeTaintsPolicy: Honor the scheduler leaves it out
# of the spread entirely, so pods pile onto whichever workers were ready first.
# Spread is decided at scheduling time and never rebalanced afterwards.
kubectl wait --for=condition=Ready nodes --all --timeout=120s >&2

kubectl apply -f k8s/engineer-crd.yaml >&2
kubectl wait --for=condition=Established crd/engineers.torkzaban.dev --timeout=60s >&2
kubectl apply -f k8s/engineer.yaml -f k8s/spread.yaml >&2
kubectl -n arman rollout status deploy/spread --timeout=120s >&2

# A rollout can succeed with pods piled onto one node (ScheduleAnyway, or a
# larger maxSkew), so check the placement itself: pods on exactly the given
# nodes, none more than one pod ahead of another, and none left Pending.
check_spread() {
  local placed want counts skew
  placed=$(kubectl -n arman get pods -l app=spread -o jsonpath='{range .items[*]}{.spec.nodeName}{"\n"}{end}' | sort)
  want=$(printf '%s\n' "$@" | sort)
  counts=$(uniq -c <<<"$placed" | awk '{print $1}' | sort -n)
  skew=$(( $(tail -1 <<<"$counts") - $(head -1 <<<"$counts") ))
  if [ "$(uniq <<<"$placed")" != "$want" ] || [ "$skew" -gt 1 ]; then
    echo "spread: want pods on $*, skew at most 1" >&2
    kubectl -n arman get pods -o wide >&2
    exit 1
  fi
}

workers=$(kubectl get nodes -l '!node-role.kubernetes.io/control-plane' -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}')
check_spread $workers

run() {
  echo "\$ $*"
  "$@"
}

echo '```console'
run kubectl get engineer arman -o wide
echo
# Warnings and the eviction log go to stderr, so to the run's log, not the README.
run kubectl drain "$off" --ignore-daemonsets
echo
# A kind node is a container, so stopping it is the power-off.
run docker stop "$off"
# The node turns NotReady once the kubelet misses its heartbeat grace period.
kubectl wait --for=condition=Ready=Unknown "node/$off" --timeout=120s >&2

# The service has to survive the power-off: every replica Ready, spread evenly
# over the workers still on.
kubectl -n arman rollout status deploy/spread --timeout=60s >&2
check_spread $(grep -vx "$off" <<<"$workers")

echo
run kubectl get nodes
echo
run kubectl -n arman get pods -o custom-columns=POD:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName
echo '```'
