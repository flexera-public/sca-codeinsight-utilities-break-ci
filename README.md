# sca-codeinsight-utilities-break-ci

The sca-codeinsight-utilities-break-ci repository is a example utility for Revenera's Code Insight product. This utility allows a user to "break" a build based on the outcome of a review by the Code Insight policy engine.   If there are one of more items rejected due to policy based on the scan results, a failing value will be returned which can then break the CI build.


**Python Requirements**

The required python modules can be installed with the use of the [requirements.txt](requirements.txt) file which can be run via.

	pip install -r requirements.txt

## Usage

Typically the execution of this script would be done as a post scan action within a CI system.  For example, within Jenkins as a post build action it is possible to add an "Execute scripts" stage.  Within this dialog it is possible to then call the included batch or shell script with three arguments
- Code Insight URL
- Code Insight Project Name
- Code Insight Authorization Token

The batch/sh file itself must also be updated for
- Path to Python 3.x
- Path to where this repository resides

## License

[MIT](LICENSE)