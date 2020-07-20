from concurrent.futures import ThreadPoolExecutor #携程 线程池
import  datetime #日期时间
import  os
from requestjsondata  import ftpfiledown


taskcount =100
threadPool = ThreadPoolExecutor(max_workers=taskcount, thread_name_prefix="test_")

root ='ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/'
urls=[
    'ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz',#1.1G
    'ALL.chr2.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz',#1.2G
    'ALL.chr3.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz',#1.0G
     'LL.chr4.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz',#1.0G
]

# ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/GRCh38_positions/ALL.chr22_GRCh38_sites.20170504.vcf.gz #30.6M  max 100
# ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/GRCh38_positions/errors/ALL.chr12_GRCh37_errors.20170504.vcf.gz 2m
url ='ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/GRCh38_positions/errors/ALL.chr12_GRCh37_errors.20170504.vcf.gz'
#url  ='ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/GRCh38_positions/ALL.chr22_GRCh38_sites.20170504.vcf.gz'
# url  ='ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/README_chrMT_phase3_callmom.md'
#url ='ftp://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/AshkenazimTrio/HG003_NA24149_father/UCSC_Ultralong_OxfordNanopore_Promethion/HG003_GRCh37_ONT-UL_UCSC_20200508.bam.bai'
url ='ftp://download.big.ac.cn/Genome/Viruses/Coronaviridae/all_protein.faa'
name ='test.gz'
for i in range(10000):
    if os.path.exists(name):
     os.remove(name)
    threadPool.submit(ftpfiledown,url,'%d%s'%(i,name))
threadPool.shutdown(wait=True)
print('sync down')
ftpfiledown(url,name)
