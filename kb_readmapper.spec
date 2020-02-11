/*
A KBase module: kb_readmapper
*/

module kb_readmapper {
    typedef structure {
        string file_name;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef readmapper(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
