# Text Encoder

Encode text provided in supported formats using one of possible encoding methods.

## Usage Examples

You can use text encoder as an imported module as well 
as from command line after adding package into ``PYTHONPATH``.

```console
C:\>python -m text_encoder --in_string="this works" --out_console --cesar --key=1 

```

## Supported encoding methods

* [Cesar code](https://en.wikipedia.org/wiki/Caesar_cipher)
* [Xor code](https://en.wikipedia.org/wiki/XOR_cipher)

## Supported inputs and outputs

* Console
* String
* File

## Design

### Available Encoders

![Class Diagram](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/meeetju/text_encoder/meeetju/start/docs/design_encoders.puml)

### Encoder Structure

![Class Diagram](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/meeetju/text_encoder/meeetju/start/docs/design_encoder.puml)

## Running the tests with coverage check

In order to enable running tests and checking
coverage execute at the command prompt:

    `pip install pytest pytest-cov`
    
To run tests and check coverage execute:

    `.\check_coverage.bat`
    
## Release history

* 1.0.0
    * First functional release
	
## License

* [LICENSE](LICENSE.md)