from mapping import Mapping

class Source(object):
    
    def __init__(self, name, mapping, biom=None, restrict=None):
        self.name = name
        self.mapping = mapping
        self.biom = biom
        self.m_cache = {}
        self.b_cache = {}
        if restrict is not None:
            new_source = self.restrict(restrict[0], restrict[1])
            self.__init__(new_source.name, new_source.mapping, biom=new_source.biom)

    def restrict(self, column, values):
        """Return a new Source object which contains only entries which have
           an entry from ``values`` in column"""
        def do_biom(p_column):
            def do_sample(c):
                sample_ids = []
                def f(value, id_, metadata):
                    is_subset = column in metadata and metadata[column] in values
                    if is_subset:
                        sample_ids.append(id_)
                    return is_subset
                biom = self.biom.filterSamples(f)
                samples = [self.mapping.get_sample(i) for i in sample_ids]
                mapping = Mapping(sample_list=samples)

                return Source(self.name, mapping, biom=biom)

            def do_obs(c):
                raise Exception("Restriction on observations are not yet implemented")

            return self._biom_if_sample_else_observation(do_sample, do_obs)

        def do_mapping(p_column):
            samples = self.mapping.get_samples(column=p_column, values=values)
            mapping = Mapping(sample_list=samples)

            biom = None
            if self.biom is not None:
                def f(value, id_, metadata):
                    return True if mapping.get_sample(id_) is not None else False
                biom = self.biom.filterSamples(f)

            return Source(self.name, mapping, biom=biom)

        return self._if_biom_else_mapping(column, do_biom, do_mapping)



    def sum_by_column(self, column, values):
        """Return a count of all samples which whos column contains an entry 
           from ``values``"""
        count = 0
        column_count = self.column_totals(column)
        for value in values:
            if value in column_count:
                count += column_count[value]
        return count

    def column_totals(self, column):
        """Return a dictionary where the key is the column value and the value
           is a count of samples"""
        return self._if_biom_else_mapping(column, self._resolve_biom_column, self._resolve_mapping_column)

    def _resolve_mapping_column(self, p_column):
        """Help ``_resolve_column``"""
        if p_column in self.m_cache:
            return self.m_cache[p_column]

        samples = self.mapping.get_samples()
        column_count = {}
        for sample in samples:
            if sample[p_column] in column_count:
                column_count[sample[p_column]] += 1
            else:
                column_count[sample[p_column]] = 1
        # These operations are expensive so lets cache it 
        self.m_cache[p_column] = column_count
        return column_count

    def _resolve_biom_column(self, p_column):
        """Help ``_resolve_column``"""
        if p_column in self.b_cache:
            return self.b_cache[p_column]

        column_count = {}

        # These operations are expensive so lets cache it 
        self.b_cache[p_column] = column_count
        return column_count

    def _validate_biom_column(self, column):
        pass

    def _if_biom_else_mapping(self, column, do_biom, do_mapping):
        p_column = ""
        tokenized = column.split(' ')
        if tokenized[0] == '@biom':
            if self.biom is None:
                raise Exception("No biom file in source '%s'" % self.name)
            p_column = column[len('@biom '):]
            return do_biom(p_column)
        elif tokenized[0] == '@mapping':
            p_column = column[len('@mapping '):]
        else:
            p_column = column
        return do_mapping(p_column)

    def _biom_if_sample_else_observation(self, column, do_sample, do_obs):
        p_column = ""
        tokenized = column.split(' ')
        if tokenized[0] == '@sample':
            p_column = column[len('@sample '):]
            return do_obs(p_column)
        elif tokenized[0] == '@observation':
            p_column = column[len('@observation '):]
        else:
            p_column = column
        return do_sample(p_column)