import os
import csv
from profile_similarity import *
from block_scheme import *
from block_clustering import *
from tqdm import tqdm
import itertools

from measure import *


if __name__ == '__main__':
    dataset_path = '../datasets/Y_Moniter'
    label_path = '../datasets/Y_Moniter_labelled_data.csv'
    brands_path = '../brands/Brands_Moniter.json'

    products = {}
    for source in tqdm(sorted(os.listdir(dataset_path))):
        for specification in sorted(os.listdir(os.path.join(dataset_path, source))):
            specification_number = specification.replace('.json', '')
            specification_id = '{}//{}'.format(source, specification_number)
            with open(os.path.join(dataset_path, source, specification_number + '.json'), encoding='utf-8') as specification_file:
                product = json.load(specification_file)

                # lower
                title = product['<page title>'].lower()
                del product['<page title>']
                for k, v in product.items():
                    product[k] = lower(v)
                product['<page title>'] = title
                if product:
                    products[specification_id] = product
    print('>>> dataset read successfully!\n')

    # match the brand
    brands, pds_with_bds, pds_without_bds, bds = MatchBrand(products, brands_path=brands_path)
    for pds in pds_with_bds.values():
        if len(pds) < 2:
            pds_without_bds.append(pds)

    # process each brand class
    results = []
    allproduct, allblocks, allentitys = {}, {}, {}
    for brand in tqdm(sorted(list(pds_with_bds.keys()))):
        product = pds_with_bds[brand]
        product.update(pds_without_bds)

        # preprocess
        new_product = {}
        for k, v in product.items():
            np = pre_process(k, v, brand)
            if np:
                new_product[k] = np
        product = new_product

        # block scheme 1 for title source
        block_scheme1 = Block_Scheme(product, 't', 'mw', 1)
        # block scheme 2 for description source
        block_scheme2 = Block_Scheme(product, 'd', 'mw', 1)
        # get blocks by block scheme aggregator
        blocks = Aggregator('+', block_scheme1, block_scheme2)
        # blocks specral clustering
        cluster_num = 3
        if len(blocks) > cluster_num:
            # when sim_method is 'KNN', sim_param is the value of k in KNN
            blocks = specralClustering(blocks, cluster_num=cluster_num, sim_method='KNN', sim_param=3, cut_method='RCut')

        # similarity and linking
        product_set = Clustering(product, blocks)

        # add record to result
        for cluster in sorted(list(product_set.values())):
            if len(cluster) < 2:
                continue
            for pair in itertools.combinations(cluster, 2):
                id_a, id_b = pair
                results.append((id_a, id_b))

        # save the block result to measure
        allproduct.update(product)
        for bid,block in blocks.items():
            allblocks[(brand,bid)] = block
        for sid,ps in product_set.items():
            allentitys[(brand,sid)] = ps

    
    # write to file
    headers = ['left_spec_id', 'right_spec_id']
    with open('submission.csv', 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(results)
    print('>>> submission.csv create successfully!\n')

    print('dataset:', 'Monitor Y')
    print('products number: ', len(allproduct))
    print('brand zones number: ', len(pds_with_bds))
    print('blocks number: ', len(allblocks))
    print('entity number: ', len(allentitys))
    print('pairs number: ', len(results))
    measure("submission.csv", label_path = label_path)

