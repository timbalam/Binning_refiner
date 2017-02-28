import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages

def GoogleVis_Sankey_plotter(input_csv, output_html, height):
    out = open(output_html, 'w')
    utils = rpackages.importr('googleVis')
    packages_needed = ['googleVis']
    for each_package in packages_needed :
        if not rpackages.isinstalled(each_package):
            utils.install_packages(each_package)
        else:
            pass

    df = robjects.DataFrame.from_csvfile(input_csv)
    # keep rows where either bin is duplicated
    i = robjects.r['duplicates'](df.rx("C1")).ro | r.objects.r['duplicates'](df.rx("C2"))
    sankey_plot = robjects.r['gvisSankey'](df.rx(i, True),
                                           option = robjects.r['list'](
                                               sankey = "{node : {colorMode: 'unique', labelPadding: 10}, link:{colorMode: 'source'}}",
                                               height = height,
                                               width = 600))
    out.write(str(sankey_plot))
    out.close()