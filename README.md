# sparqRL

### Instructions

##### To get access to provate PYPI repo - you need to do this once per conda/venv
pip install --upgrade keyring keyrings.google-artifactregistry-auth
gcloud auth login
##### You need to instal tsrex seperateley as it will cause some downstream dependencies otherwise
pip install --upgrade --extra-index-url https://europe-west2-python.pkg.dev/dsq-components/dsq-components/simple \
 'tsrex==0.3.dev3'

pip install --upgrade --extra-index-url https://europe-west2-python.pkg.dev/dsq-components/dsq-components/simple  .
##### Install lolcal requirements:
pip install -r requirements-local.txt

##### to install `dsq.gal.simulation` in dev mode:
pip install -e  .

To run a particular file
`python -m sparqRL.path.to.file`
