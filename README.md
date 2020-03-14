# Text Encoder

Encode text provided in supported formats using one of possible encoding methods.

## Usage Examples

You can use text encoder as an imported module as well 
as from command line.

As a module:

    from text_encoder.encoder import Encoder
    
    encoded_message = Encoder(FileReader("c:\text.txt"), ConsoleWriter(), Cesar(2))

From command line:

    python encoder --in_string="secret" --out_file=="d:\top_secret.txt" --cesar --key=2
    
Input and output text may be one of following:
* String
* File
* Console

## Supported encoding methods

* [Cesar code](https://en.wikipedia.org/wiki/Caesar_cipher)
* [Xor code](https://en.wikipedia.org/wiki/XOR_cipher)

## Design

![Class Diagram](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/meeetju/text_encoder/meeetju/start/docs/design.puml)

## Running the tests with coverage check

In order to enable running tests and checking
coverage execute at the command prompt:

    `pip install pytest pytest-cov`
    
To run tests and check coverage execute:

    `.\check_coverage.bat`
    
## Release history

* 0.0.1
    * Work in progres
	
## License


* [LICENSE](LICENSE.md)