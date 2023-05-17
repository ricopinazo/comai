# Comai - The AI powered terminal assistant

`comai` is an open source terminal assistant powered by OpenAI API that enables you to interact with your command line interface using natural language instructions. It simplifies your workflow by converting natural language queries into executable commands. No more memorizing complex syntax. Just chat with `comai` using plain English!

## Installation 🚀

Getting `comai` up and running is a breeze. Simply use `pip` to install the latest tested version:

```shell
pip install comai
```

The first time you run it, it'll ask you for an OpenAI API key. You can create a developer account [here](https://platform.openai.com/overview). Once in your account, go to `API Keys` section and `Create new secret key`. We recommend setting a usage limit under `Billing`/`Usage limits`.

## Usage Examples 🎉

Using `comai` is straightforward. Simply invoke the `comai` command followed by your natural language instruction. `comai` will provide you with the corresponding executable command, which you can execute by pressing Enter or ignore by pressing any other key.

Let's dive into some exciting examples of how you can harness the power of `comai`:

1. Unleash your creativity with an ASCII art cow:
```shell
$ comai print a cow saying Moo!
💡≫ echo "Moo!" | cowsay
```

2. Update the main branch and merge it into the current branch:
```shell
$ comai update the main branch and merge it into the current
💡≫ git checkout main; git pull; git checkout -; git merge main
```


3. Check the weather forecast for your location:
```shell
$ comai show me the weather forecast
💡≫ curl wttr.in
```

3. Find the annoying process using the port 8000:
```shell
$ comai show me the process using port 8000
💡≫ lsof -i :8000
```

4. Discover your future with a fortune cookie quote:
```shell
$ comai give me a fortune cookie quote
💡≫ fortune cookie
```

These are just a few examples of how `comai` can help you harness the power of the command line and provide you with useful and entertaining commands. Feel free to explore and experiment with the commands generated by `comai` to discover more exciting possibilities!

## License 📜

Comai is licensed under the GPLv3. You can find the full text of the license in the [LICENSE](./LICENSE) file.
