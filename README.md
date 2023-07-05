# Graph Generator
The Graph Generator is responsible for generating the service provider network


## Run Locally

### Checkout the project
```zsh
git clone https://github.com/Graph-Analyzer/graph-generator.git
```

### Configuration
No config required

### Run

```zsh
poetry init
poetry install
poetry run uvicorn src.main:app --reload --port 8082
```

### Access

- [Swagger](http://localhost:8082/docs)
- [API](http://localhost:8082/)

## Formatting
You can format the code with the following command.

```zsh
poetry run black src tests
```

## Authors

- [@lribi](https://github.com/lribi)
- [@pesc](https://github.com/pesc)

## License

This project is licensed under the [MIT](https://github.com/Graph-Analyzer/graph-generator/blob/main/LICENSE) License.

### Third Party Licenses

Third party licenses can be found in `THIRD_PARTY_LICENSES.txt`.

Regenerate them with this command.

```zsh
poetry export > requirements.txt

# Replace <VirtualEnvPythonPath> with the path to the python executable found with "poetry env info --path"
poetry run python -m third_party_license_file_generator -r requirements.txt -p <VirtualEnvPythonPath> -o THIRD-PARTY-LICENSES.txt

rm requirements.txt
```
