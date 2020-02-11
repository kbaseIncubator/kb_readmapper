# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
from kb_readmapper.mapper import mapper
from kb_readmapper.CachingUtils import CachingUtils


#END_HEADER


class kb_readmapper:
    '''
    Module Name:
    kb_readmapper

    Module Description:
    A KBase module: kb_readmapper
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.config = config
        self.version = 2
        #END_CONSTRUCTOR
        pass


    def readmapper(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "file_name" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN readmapper
        caching = CachingUtils(self.config)
        cache_data = {
          "reads": sorted(params["reads"]),
          "assembly_ref": params["assembly_ref"],
          "version": self.version
        }
        cache_id = caching.get_cache_id(ctx['token'], cache_data)
        result = caching.download_cache_string(ctx['token'], cache_id)
        if not result:
            tsv_file = mapper(params, callback=self.callback_url)
            with open(tsv_file) as f:
                data = f.read()
            caching.upload_to_cache(ctx['token'], cache_id, data)
        else:
            # load as json
            tsv_file = '/kb/module/work/tmp/depth.tsv'
            clean=result[1:-1].replace('\\t', '\t').replace('\\n', '\n')
            with open(tsv_file, 'w') as f:
                f.write(clean)

        output = {'file_name': tsv_file}

        #END readmapper

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method readmapper return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
