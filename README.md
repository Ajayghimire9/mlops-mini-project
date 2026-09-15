# ReviewOps

Local model training and controlled promotion.

ReviewOps demonstrates a small model lifecycle using review-text classification: train a candidate, evaluate it, verify its artifact and promote a version explicitly.

## Run locally

Use Python 3.11 or newer in a virtual environment.

```bash
pip install -r requirements-portfolio.txt
python -m reviewops.pipeline --data examples/texts.csv
```

## Design decisions

The fitted TF-IDF and logistic-regression pipeline is stored as one artifact with source and model hashes.

reviewops.promote.promote(candidate, registry, minimum_f1) checks artifact integrity and a configured quality gate before updating the champion pointer.

Immutable version directories are keyed by the model hash. The local champion pointer is replaced atomically.

Original Flask, DVC and remote-registry experiments remain available separately; the new workflow runs without credentials.

## Technology

Python, scikit-learn, joblib, local artifact registry, DVC stage definition, pytest.

## Validation

Run `python -m pytest tests -q` from the repository root. CI runs the maintained test suite and lint checks. Tests use local fixtures or mocks and do not deploy cloud resources.

## Scope and limitations

The sample reviews are smoke-test fixtures. A passing score on them is not evidence of generalisation. The promotion gate demonstrates mechanics; repeated production selection requires a separate release-validation dataset. The local registry assumes a single writer and trusted artifacts.
