# Running and releasing RetainWise

**Live status: deployed and browser-verified on 25 October 2026.**

[Open RetainWise on Streamlit](https://retainwise-employee-attrition-insights-ckdeseustexxvlbbilmnna.streamlit.app/).

An unauthenticated browser check confirmed the overview figures (1,470 records, 237 attrited, 16.1%), all five page headings, navigation and filter reset, with no visible application exceptions. The app renders inside a Streamlit frame; the earlier outer-page-only check incorrectly appeared blank. This is a hosted smoke check, not a complete repeat of local accessibility or responsive testing. The exact running commit was not independently exposed by the host.

The app was accessible without signing in during this check. The source repository and project board remain private; arrange assessor access separately.

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

No deployment credential is embedded in source. Recheck the hosted dashboard after runtime changes and confirm assessor access before submission.

## Container alternative

```sh
docker build -t retainwise .
docker run --rm -p 8501:8501 retainwise
```

The container listens on port 8501 or the hosting provider's PORT setting. It runs as the non-root appuser and uses the same port for its health check. The local Linux image has been built and exercised: the health endpoint and all five pages passed. This is runtime verification, not a public deployment.

## Render blueprint

`render.yaml` defines a Docker web service on the free plan, with the Streamlit health endpoint and automatic deployment disabled. The configuration follows [Render's blueprint specification](https://render.com/docs/blueprint-spec). Before creating a service, connect the hosting account to the private GitHub repository owned by `chasimarshad-bot`.

Create the service from the blueprint, confirm that the selected plan is free, deploy the reviewed main revision, and wait for a successful health check. Record the returned HTTPS address and deployed revision here and in the README only after opening every page and checking filter/reset behaviour. Confirm that the assessor can access the hosted app and source evidence. No service has been created while hosting access is unavailable.

## Release gate

Run notebooks from clean kernels, tests and the browser review; inspect source notices, secrets and local paths; confirm the board and documentation match reality; verify the hosted commit and navigation; then tag a reviewed release. Keep the previous working release for rollback.

## Enable continuous checks

`docs/ci-workflow.yml` is a ready-to-enable GitHub Actions template. The owner's saved token has repo and project scopes but lacks workflow scope, so the template has not been installed as an active workflow. After the owner authorises workflow access or adds the file through GitHub, copy it to `.github/workflows/qa.yml`, commit and verify its first run. No remote CI success is claimed.
