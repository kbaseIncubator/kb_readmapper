from installed_clients.ReadsUtilsClient import ReadsUtils
from installed_clients.AssemblyUtilClient import AssemblyUtil
import subprocess



SCR = '/kb/module/depth.sh'

def mapper(params, callback=None):
    reads = params['reads']
    assembly_upa = params['assembly_ref']
    ru = ReadsUtils(callback)
    reads_files = []
    for reads_upa in reads:
        reads_info = ru.download_reads({
            'read_libraries': [reads_upa],
            'interleaved': 'true',
            'gzipped': None
        })['files'][reads_upa]
        reads_files.append(reads_info)
        
    au = AssemblyUtil(callback)
    contig_file = au.get_assembly_as_fasta({'ref':assembly_upa}).get('path')

    output_file = '/kb/module/work/tmp/depth.tsv'

    command = [SCR, reads_files[0]['files']['fwd'], contig_file, output_file]

    print('In working directory: ' + ' '.join(command))
    print('Running: ' + ' '.join(command))

    p = subprocess.Popen(command, cwd='/kb/module/work/tmp', shell=False)
    exitCode = p.wait()
    if exitCode:
        raise ValueError("mapping and depth cacluation failed")
    return output_file


#[{'read_count': 772216, 'total_bases': 77221600, 'insert_size_mean': None, 'qual_min': 10.0, 'strain': None, 'sequencing_tech': 'Illumina', 'number_of_duplicates': 27220, 'base_percentages': {'A': 16.7442, 'C': 33.2539, 'T': 16.7375, 'G': 33.2643, 'N': 0.0}, 'qual_max': 51.0, 'source': None, 'single_genome': 'true', 'qual_stdev': 10.5434, 'ref': '13999/4/1', 'files': {'fwd_name': 'rhodo.art.q10.PE.reads.fastq.gz', 'fwd': '/kb/module/work/tmp/5f21ebe6-8a94-48f7-ae96-3762f1da8814.inter.fastq', 'rev': None, 'rev_name': None, 'otype': 'interleaved', 'type': 'interleaved'}, 'phred_type': '33', 'read_length_stdev': 0.0, 'read_size': None, 'qual_mean': 43.0458, 'read_length_mean': 100.0, 'insert_size_std_dev': None, 'read_orientation_outward': 'false', 'gc_content': 0.665182}]Name                     Stmts   Miss  Cover

