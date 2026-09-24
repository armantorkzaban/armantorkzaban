#!/usr/bin/env bash
# Stand up the profile cluster, check the pod spread, and print the README block on stdout.
set -euo pipefail
cd "$(dirname "$0")/.."

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
# larger maxSkew), so check the placement itself: every worker used, and no
# worker more than one pod ahead of another.
counts=$(kubectl -n arman get pods -l app=spread -o jsonpath='{range .items[*]}{.spec.nodeName}{"\n"}{end}' | sort | uniq -c | awk '{print $1}' | sort -n)
workers=$(kubectl get nodes -l '!node-role.kubernetes.io/control-plane' --no-headers | wc -l | tr -d ' ')
used=$(echo "$counts" | wc -l | tr -d ' ')
skew=$(( $(echo "$counts" | tail -1) - $(echo "$counts" | head -1) ))
if [ "$used" -ne "$workers" ] || [ "$skew" -gt 1 ]; then
  echo "spread: pods on $used of $workers workers, skew $skew" >&2
  kubectl -n arman get pods -o wide >&2
  exit 1
fi

run() {
  echo "\$ $*"
  "$@"
}

echo '```console'
run kubectl get engineer arman -o wide
echo
run kubectl get nodes
echo
run kubectl -n arman get pods -o custom-columns=POD:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName
echo '```'
