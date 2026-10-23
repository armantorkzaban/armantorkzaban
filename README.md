### Arman Torkzaban

Platform engineer in Göttingen. I work on Kubernetes, the Linux underneath it, and the pipelines
that keep both honest. Right now I'm building [Wattproof](https://wattproof.de), to make clusters on
your own hardware use less power, and prove it. I also build infrastructure for civic tech that
has to keep working when someone is trying to switch it off.

<!-- cluster:start -->
```console
$ kubectl get engineer arman -o wide
NAME    ROLE                LOCATION     FOCUS
arman   platform-engineer   göttingen    k8s scheduling · energy · gitops · civic-tech infra

$ kubectl drain profile-worker3 --ignore-daemonsets
node/profile-worker3 cordoned
evicting pod arman/spread-77fb9db889-vp9d6
pod/spread-77fb9db889-vp9d6 evicted
node/profile-worker3 drained

$ docker stop profile-worker3
profile-worker3

$ kubectl get nodes
NAME                    STATUS                        ROLES           AGE   VERSION
profile-control-plane   Ready                         control-plane   80s   v1.37.0
profile-worker          Ready                         <none>          65s   v1.37.0
profile-worker2         Ready                         <none>          65s   v1.37.0
profile-worker3         NotReady,SchedulingDisabled   <none>          65s   v1.37.0

$ kubectl -n arman get pods -o custom-columns=POD:.metadata.name,NODE:.spec.nodeName
POD                       NODE
spread-77fb9db889-d9pq8   profile-worker2
spread-77fb9db889-fv4cl   profile-worker
spread-77fb9db889-mrtrl   profile-worker
spread-77fb9db889-n6fpg   profile-worker2
```
<sub>Real output from a kind cluster, rebuilt daily by <a href="https://github.com/armantorkzaban/armantorkzaban/actions/runs/39881399703">this run</a>. One worker is drained and switched off, and the run fails if the pods don't spread evenly over the rest. Wattproof will do this to real servers.</sub>
<!-- cluster:end -->

#### Building

**[Wattproof](https://github.com/wattproof/wattproof)** (in design) · [wattproof.de](https://wattproof.de)\
Lowers the power a Kubernetes cluster draws at the wall without breaking its service levels: it rightsizes workloads, keeps the most efficient servers on, and powers the rest down until they're needed.
Every saving is metered and proven in an experiment anyone can re-run from the published data.

**[Beh.dev](https://beh.dev)**\
My one-person AI company, set up like a city. Every agent has a written role, a budget and someone
who reviews its work, and nothing leaves the network unless it's allowed to. Most of it is still on
paper. So far it ships [Selfwise](https://selfwise.space) and [Juju](https://juju.beh.dev), a
picture-story app that teaches children their family's language.

#### Research

At the [L3S Research Center](https://www.l3s.de) I worked on two EU Horizon projects,
[GLACIATION](https://github.com/glaciation-heu) and [CLEVER](https://www.cleverproject.eu/). I wrote
Kubernetes scheduler plugins in Go, driven by a reinforcement-learning engine. Wattproof grew out of what I learned there: measure the
machines you optimise, and compare against a strong baseline. Public work:
[IceStream](https://github.com/glaciation-heu/IceStream) and the
[GitOps deployments](https://github.com/glaciation-heu/gitops-deployments).

#### Civic tech

- **[Jomhoor](https://jomhoor.org)**, anonymous and verifiable voting. A
  [wallet](https://github.com/jomhoor/Jomhoor-wallet) that proves you can vote from your passport
  without your data leaving the phone, and an
  [STV simulator](https://github.com/jomhoor/STV-voting-simulator) anyone can use to re-check a count.
- **[Atlas Iran](https://atlasiran.org)**. A
  [directory of Iranian civil-society organisations](https://github.com/Atlasiran/Atlas-website),
  [34 constitutions](https://github.com/Atlasiran/constitutions) compared article by article, and
  [normalcy](https://github.com/jomhoor/normalcy), a human-rights benchmark.

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
