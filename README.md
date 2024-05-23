<div align="center">
  <img src="https://raw.githubusercontent.com/ricopinazo/comai/main/logo.svg" alt="comai" width="200"/>

**The AI powered terminal assistant**

[![Tests](https://github.com/ricopinazo/comai/actions/workflows/tests.yml/badge.svg)](https://github.com/ricopinazo/comai/actions/workflows/tests.yml)
[![Latest release](https://img.shields.io/github/v/release/ricopinazo/comai?color=brightgreen&include_prereleases)](https://github.com/ricopinazo/comai/releases)
[![PyPI](https://img.shields.io/pypi/v/comai)](https://pypi.org/project/comai/)
[![Issues](https://img.shields.io/github/issues/ricopinazo/comai?color=brightgreen)](https://github.com/ricopinazo/comai/issues)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/comai)](https://pypi.org/project/comai/)
[![License GPLv3](https://img.shields.io/badge/license-GPLv3-blue.svg)](./LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

</div>

## What is comai? 🎯

`comai` is an open source CLI utility that translates natural language instructions into executable commands.

<div align="left">
<img src="https://raw.githubusercontent.com/ricopinazo/comai/627d94d39430bb574582f51cc64700012e9c28ce/demo.gif" alt="demo" width="350"/>
</div>

## Installation 🚀

`comai` is available as a python package. We recommend using [`pipx`](https://pypa.github.io/pipx/) to install it:

```shell
pipx install comai
```

By default, `comai` is setup to use [ollama](https://ollama.com) under the hood, which allows you to host any popular open source LLM locally. If you are happy with this, make sure to install and have ollama running. You can find the install instructions [here](https://ollama.com/download).

Once installed, make sure to download the `llama3` model, since comai has been optimised for it

```shell
ollama pull llama3
```

Otherwise, you can set up any other model available in the ollama service via:

```shell
comai --config
```

> **_NOTE:_** `comai` uses the environment variable `TERM_SESSION_ID` to maintain context between calls so you don't need to repeat yourself giving instructions to it. You can check if it is available in your default terminal checking the output of `echo $TERM_SESSION_ID`, which should return some type of UUID. If the output is empty, you can simply add the following to your `.zshrc`/`.bashrc` file:
>
> ```shell
> export TERM_SESSION_ID=$(uuidgen)
> ```

## Usage examples 🎉

Using `comai` is straightforward. Simply invoke the `comai` command followed by your natural language instruction. `comai` will provide you with the corresponding executable command, which you can execute by pressing Enter or ignore by pressing any other key.

Let's dive into some exciting examples of how you can harness the power of `comai`:

1. Access network details:

```
$ comai print my public ip address
❯ curl -s4 ifconfig.co
92.234.58.146
```

2. Manage `git` like a pro:

```shell
$ comai rename the current branch to awesome-branch
❯ git branch -m $(git rev-parse --abbrev-ref HEAD) awesome-branch

$ comai show me all the branches having commit c4c0d2d in common
❯ git branch -a --contains c4c0d2d
  main
  fix/terrible-bug
* awesome-branch
```

3. Find the annoying process using the port 8080:

```shell
$ comai show me the process using the port 8080
❯ lsof -i :8080
COMMAND   PID      USER   FD   TYPE            DEVICE SIZE/OFF NODE NAME
node    36350 pedrorico   18u  IPv4 0xe0d28ea918e376b      0t0  TCP *:http-alt (LISTEN)
```

4. Get rid of all your docker containers:

```shell
$ comai stop and remove all running docker containers
❯ docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
```

## Contributions welcome! 🤝

If you're interested in joining the development of new features for `comai`, here's all you need to get started:

1. Clone the [repository](https://github.com/ricopinazo/comai) and navigate to the root folder.
2. Install the package in editable mode by running `pip install -e .`.
3. Run the tests using `pytest`.
4. Format your code using [black](https://github.com/psf/black) before submitting any change.

## License 📜

Comai is licensed under the GPLv3. You can find the full text of the license in the [LICENSE](./LICENSE) file.
