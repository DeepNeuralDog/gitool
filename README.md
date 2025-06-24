# gitool

A command line tool to make using Git easier.

## Installation

### 1. Install pipx

#### On macOS (with Homebrew)
```sh
brew install pipx
pipx ensurepath
```

#### On Linux
```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```
> `pipx ensurepath` for ensuring installation

---

### 2. Install gitool


#### From a local clone (for development)
In the project root:
```sh
git clone https://github.com/DeepNeuralDog/gitool.git && cd git
pipx install .
```


#### Directly from GitHub (if you publish your repo)
```sh
pipx install git+https://github.com/DeepNeuralDog/gitool.git
```

---

## Usage

After installation, the following commands are available globally:

- `gtool` — Main entry point (nothing for now)
- `acp` — Add, Commit, and Push in one go
- `gnew` — Create a new local and connect remote repository


