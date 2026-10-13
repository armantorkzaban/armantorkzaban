### Arman Torkzaban

Platform engineer in Göttingen. Kubernetes, the Linux underneath it, and the pipelines that keep
both honest. Now building [Wattproof](https://wattproof.de), which lowers the power a cluster draws
at the wall and proves the saving. Alongside it, infrastructure for civic tech that has to keep
working when someone is actively trying to switch it off.

<!-- cluster:start -->
```console
$ kubectl get engineer arman -o wide
NAME    ROLE                LOCATION     FOCUS
arman   platform-engineer   göttingen    k8s scheduling · energy · gitops · civic-tech infra

$ kubectl drain profile-worker3 --ignore-daemonsets
node/profile-worker3 cordoned
evicting pod arman/spread-77fb9db889-k82b9
pod/spread-77fb9db889-k82b9 evicted
node/profile-worker3 drained

$ docker stop profile-worker3
profile-worker3

$ kubectl get nodes
NAME                    STATUS                        ROLES           AGE   VERSION
profile-control-plane   Ready                         control-plane   83s   v1.37.0
profile-worker          Ready                         <none>          73s   v1.37.0
profile-worker2         Ready                         <none>          73s   v1.37.0
profile-worker3         NotReady,SchedulingDisabled   <none>          72s   v1.37.0

$ kubectl -n arman get pods -o custom-columns=POD:.metadata.name,NODE:.spec.nodeName
POD                       NODE
spread-77fb9db889-5vx7l   profile-worker
spread-77fb9db889-6bq8t   profile-worker2
spread-77fb9db889-7dqzd   profile-worker
spread-77fb9db889-kcbwp   profile-worker2
```
<sub>Real output from a kind cluster, rebuilt daily by <a href="https://github.com/armantorkzaban/armantorkzaban/actions/runs/38347674264">this run</a>. The run fails unless every replica is Ready and evenly spread over the workers still on. Wattproof does the same to real servers, and meters the watts.</sub>
<!-- cluster:end -->

#### Building

**[Wattproof](https://github.com/wattproof/wattproof)** · [wattproof.de](https://wattproof.de) · Go, Python\
Keeps a cluster's most efficient servers on, drains and powers off the rest, and powers them on
again before demand returns. Stock Kubernetes only: taints, the eviction API, PodDisruptionBudgets.
Power is metered at the wall, and a claimed saving has to pass a randomised, pre-registered
experiment against two baselines: stock Kubernetes, and a tuned open-source setup. Design and
simulation so far. The [lab notebook](https://github.com/wattproof/wattproof/tree/main/docs/notebook)
publishes the negative results too.

**[Beh.dev](https://beh.dev)** · a personal AI company, built like a city\
Agents are declarative specs: purpose, tools, data clearance, budget, and who reviews their work.
The city runs on k3s and NATS JetStream with default-deny egress, so exfiltration is a routing
impossibility rather than a promise. Most of it is designed, not yet built, and
[the architecture page](https://beh.dev/city/) says which. It ships [Selfwise](https://selfwise.space),
which maps how you think, and [Juju](https://juju.beh.dev), picture-stories that teach a child
their family's language.

#### Research

At the [L3S Research Center](https://www.l3s.de) I worked on two EU Horizon projects,
[GLACIATION](https://github.com/glaciation-heu) and [CLEVER](https://www.cleverproject.eu/). I wrote
custom Kubernetes scheduler plugins in Go, driven by a reinforcement-learning decision engine, and
built the telemetry pipelines on EKS, Prometheus and Grafana that fed it. Wattproof starts from
what that taught me: measure the machines you optimise, and test against a strong baseline. Public
work: [IceStream](https://github.com/glaciation-heu/IceStream) and the
[GitOps deployments](https://github.com/glaciation-heu/gitops-deployments).

#### Civic tech

- **[Jomhoor](https://jomhoor.org)**, anonymous and verifiable voting. A [wallet](https://github.com/jomhoor/Jomhoor-wallet)
  that proves eligibility from a passport's chip with zero-knowledge proofs, the data never leaving
  the phone; [relayers](https://github.com/jomhoor/Platform) anchored to Rarimo L2; and an
  [STV simulator](https://github.com/jomhoor/STV-voting-simulator) anyone can use to re-count a
  published result.
- **[Atlas Iran](https://atlasiran.org)**. A bilingual, right-to-left
  [directory of civil society](https://github.com/Atlasiran/Atlas-website),
  [34 constitutions](https://github.com/Atlasiran/constitutions) split into articles and compared
  side by side, and [normalcy](https://github.com/jomhoor/normalcy), a human-rights benchmark of
  citable provisions.
- **[Digital Freedom Congress](https://difcongress.com)**. A
  [site in six languages](https://github.com/Iran-Digital-Freedom-Congress/the-digital-congress),
  built from one CSV of strings.

#### Stack

```text
delivery       GitHub Actions · Argo CD · Helm
orchestration  Kubernetes · scheduler plugins in Go
provisioning   Terraform / OpenTofu · AWS (EKS, EC2, IAM, VPC)
os             Linux internals · cgroups · hardening · Talos
metal          Redfish · BMCs · metered PDUs

observability  Prometheus · Grafana · OpenTelemetry
languages      Go · Python · TypeScript · Bash
```

---

[armantorkzaban.com](https://armantorkzaban.com) · [wattproof.de](https://wattproof.de) · [beh.dev](https://beh.dev) · [jomhoor.org](https://jomhoor.org)
