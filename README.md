### Arman Torkzaban

Platform engineer in Göttingen. Kubernetes, the Linux underneath it, and the pipelines that keep
both honest. I build infrastructure for civic tech that has to keep working when someone is
actively trying to switch it off.

<!-- cluster:start -->
```console
$ kubectl get engineer arman -o wide
NAME    ROLE                LOCATION     FOCUS
arman   platform-engineer   göttingen    k8s scheduling · gitops · observability · civic-tech infra

$ kubectl get nodes
NAME                    STATUS   ROLES           AGE   VERSION
profile-control-plane   Ready    control-plane   28s   v1.37.0
profile-worker          Ready    <none>          18s   v1.37.0
profile-worker2         Ready    <none>          18s   v1.37.0
profile-worker3         Ready    <none>          18s   v1.37.0

$ kubectl -n arman get pods -o custom-columns=POD:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName
POD                       STATUS    NODE
spread-77fb9db889-bfcr6   Running   profile-worker2
spread-77fb9db889-jshtd   Running   profile-worker
spread-77fb9db889-kfjff   Running   profile-worker3
spread-77fb9db889-xcd29   Running   profile-worker
```
<sub>Real output from a kind cluster, rebuilt daily by <a href="https://github.com/armantorkzaban/armantorkzaban/actions/runs/36206828529">this run</a>.</sub>
<!-- cluster:end -->

**Research.** At the L3S Research Center I worked on two EU Horizon projects,
[GLACIATION](https://github.com/glaciation-heu) and [CLEVER](https://www.cleverproject.eu/). I wrote custom Kubernetes scheduler
plugins in Go, driven by a reinforcement-learning decision engine, and built the telemetry
pipelines on EKS, Prometheus and Grafana that fed the engine. Public work from that time:
[IceStream](https://github.com/glaciation-heu/IceStream) and the project's
[GitOps deployments](https://github.com/glaciation-heu/gitops-deployments).

**Now.** I'm building [Selfwise](https://selfwise.space), a privacy-first AI platform on the edge,
and I help run [Jomhoor](https://jomhoor.org), a platform for anonymous, verifiable voting.

#### Things I built

| Project | What it is | Stack |
|---|---|---|
| [STV voting simulator](https://github.com/jomhoor/STV-voting-simulator) · [live](https://jomhoor.github.io/STV-voting-simulator/) | Single Transferable Vote with reserved seats and a tie-break fixed before counting. Regression-tested against the reference paper, and runs from the CLI so anyone can check a published result. | TypeScript |
| [Jomhoor wallet](https://github.com/jomhoor/Jomhoor-wallet) | Mobile wallet that reads passports and national ID cards over NFC and proves eligibility with zero-knowledge proofs. The document data never leaves the phone. | TypeScript, Noir, Circom |
| [Jomhoor platform](https://github.com/jomhoor/Platform) | Relayers for registration and vote submission behind an nginx gateway, anchored to Rarimo L2. | Solidity, Docker |
| [Digital Freedom Congress](https://github.com/Iran-Digital-Freedom-Congress/the-digital-congress) · [live](https://difcongress.com) | Static site in six languages, built from a single CSV of strings, including right-to-left scripts. | HTML, Python |
| [Atlas of Iranian civil society](https://github.com/Atlasiran/Atlas-website) · [live](https://atlasiran.org) | Bilingual, RTL-first SvelteKit directory of civil-society organisations. | SvelteKit, Supabase, Cloudflare |
| [Iranian constitutions corpus](https://github.com/Atlasiran/constitutions) · [live](https://atlasiran.org/constitutions#corpus) | 34 constitutions and political programmes, split into articles and compared side by side. The 1979 constitution is assessed like any other, never as the reference. | Python, Tesseract |
| [normalcy](https://github.com/jomhoor/normalcy) · [live](https://normalcy.is) | Human-rights benchmark for Atlas and Jomhoor: twelve international instruments split into citable provisions. Claude audits documents against them; every citation is verified and a human reviews before publishing. | TypeScript, Cloudflare Workers |

#### Organisations

<a href="https://github.com/jomhoor"><img src="https://github.com/jomhoor.png?size=80" width="40" alt="Jomhoor" title="Jomhoor"></a>
<a href="https://github.com/Iranians-Vote-Digital-Democracy"><img src="https://github.com/Iranians-Vote-Digital-Democracy.png?size=80" width="40" alt="Iranians.Vote" title="Iranians.Vote"></a>
<a href="https://github.com/tcfev"><img src="https://github.com/tcfev.png?size=80" width="40" alt="Transnational Community Federation" title="Transnational Community Federation e.V."></a>
<a href="https://github.com/Atlasiran"><img src="https://github.com/Atlasiran.png?size=80" width="40" alt="Atlas Iran" title="Atlas Iran"></a>
<a href="https://github.com/Iran-Digital-Freedom-Congress"><img src="https://github.com/Iran-Digital-Freedom-Congress.png?size=80" width="40" alt="Iran Digital Freedom Congress" title="Iran Digital Freedom Congress"></a>
<a href="https://github.com/glaciation-heu"><img src="https://github.com/glaciation-heu.png?size=80" width="40" alt="GLACIATION" title="GLACIATION (EU Horizon)"></a>

#### Toolbox

Kubernetes (scheduler plugins, Helm, ArgoCD) · AWS (EKS, EC2, IAM, VPC) · Terraform / OpenTofu ·
Prometheus, Grafana, OpenTelemetry · Linux internals and hardening · Go, Python, TypeScript, Bash

#### Active lately

<!-- activity:start -->
| Repository | Commits (90d) | About |
|---|--:|---|
| [armantorkzaban/armantorkzaban.github.io](https://github.com/armantorkzaban/armantorkzaban.github.io) | 35 |  |
| [Atlasiran/constitutions](https://github.com/Atlasiran/constitutions) | 26 | Iranian constitutions and constitutional proposals: corpus, article-level comparison and human-rights benchmark |
| [Atlasiran/Atlas-website](https://github.com/Atlasiran/Atlas-website) | 15 | Iranian Civil Society Organisations |
| [jomhoor/STV-voting-simulator](https://github.com/jomhoor/STV-voting-simulator) | 9 |  |
| [jomhoor/normalcy](https://github.com/jomhoor/normalcy) | 7 | Jomhoor's Normative Compliancy System |
| [jomhoor/Jomhoor.org](https://github.com/jomhoor/Jomhoor.org) | 5 | جمهور Rebuplic |

Plus 548 contributions to private repositories.
<!-- activity:end -->

<sub>Generated daily by <a href="scripts/activity.py">scripts/activity.py</a>. Private work is counted, never named.</sub>

#### When I commit

<!-- habits:start -->
```text
hour  00  04  08  12  16  20
      █▇█▅▄▂▅▂▂▂▄▃▂▂▃▃▂▃▅▃▅▅▆█   peak 00:00

day   M T W T F S S
      █ █ ▆ █ █ ▄ ▇   peak Tue
```
<sub>529 public commits over the last 365 days, by author time in Europe/Berlin.</sub>
<!-- habits:end -->

#### By the numbers

<img src="/github-metrics.svg" alt="GitHub metrics: contribution calendar, languages, featured repositories">

---

[armantorkzaban.com](https://armantorkzaban.com) · [jomhoor.org](https://jomhoor.org) · [selfwise.space](https://selfwise.space)
