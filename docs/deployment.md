# Running and releasing RetainWise

**Live status: not deployed.** Local application checks do not establish a public deployment. No live URL is claimed.

## Local run

Use Python 3.12.8. From the repository root:

```powershell
py -3.12 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m streamlit run app.py
```

The reviewed v1 dataset is committed; no Kaggle credentials or notebook execution are needed to open the app.

## Streamlit Community Cloud

1. Sign in at https://share.streamlit.io/ with the repository owner's account, `chasimarshad-bot`.
2. Authorise access to this private repository if the hosting service supports the account's selected access configuration. Do not make the repository public merely to bypass access problems.
3. Select repository `chasimarshad-bot/RetainWise-Employee-Attrition-Insights`, branch `main`, entrypoint `app.py`, and Python 3.12.
4. Deploy without secrets. Confirm all five pages, filters, an empty selection, figures and external links on the hosted app.
5. Record the returned URL in the README and this file, note the tested commit, and confirm access settings before claiming release.

This environment has GitHub credentials but no authenticated Streamlit hosting session. The available Sites host supports Cloudflare Workers rather than a persistent Python Streamlit server. No deployment credential has been requested or embedded in source.

## Container alternative

```sh
docker build -t retainwise .
docker run --rm -p 8501:8501 retainwise
```

The container listens on port 8501 or the hosting provider's PORT setting. Deploy it to an authorised Python/container service, configure HTTPS and access controls, and verify the health endpoint `/_stcore/health`. Container instructions are not a claim that an image has been built or deployed here.

## Release gate

Run notebooks from clean kernels, tests and the browser review; inspect source notices, secrets and local paths; confirm the board and documentation match reality; verify the hosted commit and navigation; then tag a reviewed release. Keep the previous working release for rollback.

## Enable continuous checks

`docs/ci-workflow.yml` is a ready-to-enable GitHub Actions template. The owner's saved token has repo and project scopes but lacks workflow scope, so the template has not been installed as an active workflow. After the owner authorises workflow access or adds the file through GitHub, copy it to `.github/workflows/qa.yml`, commit and verify its first run. No remote CI success is claimed.
