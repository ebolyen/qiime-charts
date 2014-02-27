
def group_by_id_factory(aliases, default):
    def group_by_id(value):
        if value in aliases:
            return aliases[value]
        else:
            return default
    return group_by_id

def group_by_bin_factory(bins, default):
    def group_by_bin(value):
        try:
            float(value)
        except ValueError:
            return default

        dif = None
        best_bin = default
        for bin in bins.iterkeys():
            if float(bin) > value:
                continue
            else:
                n_dif = value - float(bin)
                if dif is None or n_dif < dif:
                    dif = n_dif
                    best_bin = bins[bin]
        return best_bin
    return group_by_bin

def get_grouper(data_dict):
    return {
        'id':lambda : group_by_id_factory(data_dict['aliases'], data_dict['default']),
        'bin':lambda : group_by_bin_factory(data_dict['bins'], data_dict['default']),
    }[data_dict['group-by']]()