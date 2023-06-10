<div align="center">
  <img src="https://raw.githubusercontent.com/ricopinazo/comai/main/logo.svg" alt="demo" width="200"/>
  
  **The AI powered terminal assistant**
  
  [![Tests](https://github.com/ricopinazo/comai/actions/workflows/tests.yml/badge.svg)](https://github.com/ricopinazo/comai/actions/workflows/tests.yml)
  [![Latest release](https://img.shields.io/github/v/release/ricopinazo/comai?color=brightgreen&include_prereleases)](https://github.com/ricopinazo/comai/releases)
  [![PyPI](https://img.shields.io/pypi/v/comai)](https://pypi.org/project/comai/)
  [![Issues](https://img.shields.io/github/issues/ricopinazo/comai?color=brightgreen)](https://github.com/ricopinazo/comai/issues)
  [![PyPI - Downloads](https://img.shields.io/pypi/dm/comai)](https://pypi.org/project/comai/)
  [![License GPLv3](https://img.shields.io/badge/license-GPLv3-blue.svg)](./LICENSE)
  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
</div>

## What is comai? 🎯

`comai` is an open source terminal assistant powered by OpenAI API that enables you to interact with your command line interface using natural language instructions. It simplifies your workflow by converting natural language queries into executable commands. No more memorizing complex syntax. Just chat with `comai` using plain English!

<div align="left">
<img src="https://raw.githubusercontent.com/ricopinazo/comai/main/demo.gif" alt="demo" width="350"/>
</div>

## Installation 🚀

Getting `comai` up and running is a breeze. You can simply use [`pip`](https://pip.pypa.io/en/stable/) to install the latest version:

```shell
pip install comai
```

However, if you usually work with python environments, it is recommended to use [`pipx`](https://pypa.github.io/pipx/) instead:

```shell
pipx install comai
```

The first time you run it, it'll ask you for an OpenAI API key. You can create a developer account [here](https://platform.openai.com/overview). Once in your account, go to `API Keys` section and `Create new secret key`. We recommend setting a usage limit under `Billing`/`Usage limits`.

> **_NOTE:_** `comai` uses the environment variable `TERM_SESSION_ID` to maintain context between calls so you don't need to repeat yourself giving instructions to it. You can check if it is available in your default terminal checking the output of `echo $TERM_SESSION_ID`, which should return some type of UUID. If the output is empty, you can simply add the following to your `.zshrc`/`.bashrc` file:
> ```shell
> export TERM_SESSION_ID=$(uuidgen)
> ```

## Usage Examples 🎉

Using `comai` is straightforward. Simply invoke the `comai` command followed by your natural language instruction. `comai` will provide you with the corresponding executable command, which you can execute by pressing Enter or ignore by pressing any other key.

Let's dive into some exciting examples of how you can harness the power of `comai`:

1. Manage your system like a pro:
```shell
$ comai print my private ip address
❯ ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}'
192.168.0.2

$ comai and my public one
❯ curl ifconfig.me
92.234.58.146
```

2. Master the intricacies of `git`:
```shell
$ comai squash the last 3 commits into a single commit
❯ git rebase -i HEAD~3

$ comai show me all the branches having commit c4c0d2d in common
❯ git branch --contains c4c0d2d
  chat-api
  configparser
* main
```

3. Check the weather forecast for your location:
```shell
$ comai show me the weather forecast
❯ curl wttr.in
```

4. Find the annoying process using the port 8080:
```shell
$ comai show me the process using the port 8080
❯ lsof -i :8080
COMMAND   PID      USER   FD   TYPE            DEVICE SIZE/OFF NODE NAME
node    36350 pedrorico   18u  IPv4 0xe0d28ea918e376b      0t0  TCP *:http-alt (LISTEN)

$ comai show me only the PID
❯ lsof -t -i :8080
36350

$ comai kill it
❯ kill $(lsof -t -i :8080)
```

5. Swiftly get rid of all your docker containers:
```shell
$ comai stop and remove all running docker containers
❯ docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
```

These are just a few examples of how `comai` can help you harness the power of the command line and provide you with useful and entertaining commands. Feel free to explore and experiment with the commands generated by `comai` to discover more exciting possibilities!

## Contributions welcome! 🤝

If you're interested in joining the development of new features for `comai`, here's all you need to get started:

1. Clone the [repository](https://github.com/ricopinazo/comai) and navigate to the root folder.
2. Install the package in editable mode by running `pip install -e .`.
3. Run the tests using `pytest`. Make sure you have the `OPENAI_API_KEY` environment variable set up with your OpenAI API key. Alternatively, you can create a file named `.env` and define the variable there.


This project utilizes black for code formatting. To ensure your changes adhere to this format, simply follow these steps:

```shell
pip install black
black .
```

For users of VS Code, you can configure the following options after installing `black`:

```json
"editor.formatOnSave": true,
"python.formatting.provider": "black"
```

## License 📜

Comai is licensed under the GPLv3. You can find the full text of the license in the [LICENSE](./LICENSE) file.
