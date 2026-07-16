# Reference - Plugin API

OmegaClaw provides the plugin API which allows writing plugins to extend the
agent's functionality. Plugin is a MeTTa or Python module which provides the
entry point - function `loadOmegaClawPlugin`. `loadOmegaClawPlugin` function
calls OmegaClaw plugin API in order to implement new agent's features. Plugin
API provides functions to:
- add communication channel integrations
- add LLM provider integrations
- add new skills or remove added skills
- extend LLM prompt by adding new information or removing it

In order to be loaded the plugin should be included into
[config/plugins.yaml](../config/plugins.yaml) file.  Agent loads each module
listed in this file on the start and calls an entry function of each loaded
module.All communication channels and LLM integrations of the OmegaClaw are
implemented using this API. The full list of plugins available in the OmegaClaw
repository can be found in the [config/plugins.yaml](../config/plugins.yaml)
file.

## Communication channel integration

In order to implement new communication channel one should implement two main
functions:
- "receive" - returns the next message received through communication channel
- "send" - sends the message through communication channel

### Python

In Python one should implement class which inherits from
`pluginapi.CommChannel` and implement at least two methods of the ancestor.

```python
import pluginapi

class ExampleCommChannel(pluginapi.CommChannel):

    def start(self) -> None:
        print("ExampleCommChannel is started")

    def stop(self) -> None:
        print("ExampleCommChannel is stopped")

    def receive(self) -> str:
        return "Received message example" 

    def send(self, message: str) -> None:
        print(f"ExampleCommChannel sends {message}")
```

In order to be able using this communication channel the plugin code should
register the instance of the `ExampleCommChannel` in the system using
`registerCommChannel` function.

```python
def loadOmegaClawPlugin(config: dict):
    pluginapi.registerCommChannel("Example", ExampleCommChannel())
```

### MeTTa

Similar approach should be used to write communication plugin in MeTTa
programming language. The difference is that in MeTTa we should use callback
registering approach instead of writing a class. First write functions which
implements the required interface and then use `register-comm-channel` function
to register callbacks.

```metta
(= (examplecommchannel-receive)
   "Received message example")

(= (examplecommchannel-send $message)
   (println! ("ExampleCommChannel sends " $message)))

(= (loadOmegaClawPlugin $config)
   (register-comm-channel "Example"
     ((start (|-> () (println! "ExampleCommChannel is started")))
      (stop (|-> () (println! "ExampleCommChannel is stopped")))
      (receive (|-> () (examplecommchannel-receive)))
      (send (|-> ($message) (examplecommchannel-send $message))))))
```

`register-comm-channel` gets list of pairs as the input. Each pair contains the
id of the callback function and the callback lambda to call. We can implement
in-place callback (`start` and `stop` examples) or call a function (`receive`
and `send` functions above). As current MeTTa interpreter used by OmegaClaw
doesn't have function scoping one need to be careful and choose the unique
function names. It is the reason why `examplecommchannel-` prefix is added to
the receive and send functions.

### Using communication channel

The first parameter of the `registerCommChannel` function is a channel id which
should be used as a value for the `commchannel` command line parameter to use
the communication channel with the agent (see
[README.md](../README.md#channels-srcchannelsmetta)):

```sh
sh run.sh run.metta commchannel=Example
```

## LLM provider integration

In order to implement new LLM provider integration one should provide
implementation of the single function `chat`. The function gets three
parameters:
- `prompt` - the string which is sent to LLM by agent as a prompt, required
- `max_tokens` - maximum number of tokens can be used by provider to answer the
  prompt, default value is 6000
- `reasoning_mode` - the reasoning mode of the LLM, default value is "medium"
functions:

### Python

In Python one should implement class which inherits from
`pluginapi.LLMProvider` and implement at least one method of the ancestor.

```python
import pluginapi

class ExampleLLMProvider(pluginapi.LLMProvider):

    def start(self) -> None:
        print("ExampleLLMProvider is started")

    def stop(self) -> None:
        print("ExampleLLMProvider is stopped")

    def chat(self, prompt: str, max_tokens: int = 6000, reasoning_mode: str = "medium") -> str:
        return "LLM answer example" 
```

In order to be able using this LLM provider integration the plugin code should
register the instance of the `ExampleLLMProvider` in the system using
`registerLLMProvider` function.

```python
def loadOmegaClawPlugin(config: dict):
    pluginapi.registerLLMProvider("Example", ExampleLLMProvider())
```

### MeTTa

Similarly to the [communication channel
example](#communication-channel-integration) we should use callback registering
approach instead of writing a class. First write functions which implements the
required interface and then use `register-llm-provider` function to register
callbacks.

```metta
(= (examplellmprovider-chat $prompt $max_tokens $reasoning_mode)
   "LLM answer example")

(= (loadOmegaClawPlugin $config)
   (register-llm-provider "Example"
     ((start (|-> () (println! "ExampleLLMProvider is started")))
      (stop (|-> () (println! "ExampleLLMProvider is stopped")))
      (chat (|-> ($prompt $max_tokens $reasoning_mode) (examplellmprovider-chat $prompt $max_tokens $reasoning_mode))))))
```

### Using LLM provider

The first parameter of the `registerLLMProvider` function is a provider id which
should be used as a value for the `provider` command line parameter to use
the LLM provider with the agent (see [README.md](../README.md#general)):

```sh
sh run.sh run.metta provider=Example
```

## Modifying set of skills


