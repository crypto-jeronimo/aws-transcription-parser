# Amazon Transcribe job parser which outputs formatted HTML

This is an automatic parser of Amazon Transcribe jobs - of podcast episodes - which outputs to HTML.

Compatible with Python 2.7 and Python 3+.

Just populate an input file, called `input.txt`, where each line is semi-colon-separated and contains the name of the Amazon Transcribe output JSON file, and a comma-separated, ordered list of speakers.

For example, the following `input.txt` file will result in the iterative processing of files `episode_1.json`, `episode_2.json` and `episode_3.json`. `speaker_1`, `speaker_2` and `speaker_3` will replace the automatically generated placeholders `spk_0`, `spk_1` and `spk_2`.
The output HTML files will be named after the `jobName` from each input JSON file.

```
episode_1.json;speaker_1,speaker_2
episode_2.json;speaker_2,speakder_3
episode_3.json;speaker_1,speaker_2,speakder_3
```

Once you've created your `input.txt` file and moved it in the same directory as the `process_aws_output.py` file, you simply need to run the script with Python:
```
$ python process_aws_output.py
SUCCESS!
```

A `SUCCESS!` message is expected, signifying that all HTML outputs have been stored in the same directory.

Please, don't hesitate to ask questions or request changes or improvements via the [Issues](https://github.com/crypto-jeronimo/aws-transcription-parser/issues) section.


If you're feeling generous, donations are welcome:

**BTC:** 1QFNgTV3GQby8uv3mXwLKBHAgKUEenSREd

**ETH:** 0xa7350d9fb3c6193759b587bb984f0dfe3568c8ed

**LTC:** LW3SNJ61CXUfRQTpehpDfV7vv1iVdLh9En

**ADA:** DdzFFzCqrhtBbS7o5LQ3u1ZxFVz3Q6b2bQ86FEYanf6UsRgK6D3So4grpZEHPXcitQWEuRfnAA7jzi3xmj9Md6kng2UiVn4QLxEsAefK

**BCH:** 1QFNgTV3GQby8uv3mXwLKBHAgKUEenSREd
