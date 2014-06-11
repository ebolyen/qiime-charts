import csv

class _AllTrue(object):
    def __contains__(self, other):
        return True

class Mapping(object):
    def __init__(self, mapping_file_object=None, sample_list=None):
        if mapping_file_object is None and sample_list is None:
            raise Exception('No source for Mapping object. Instantiation requires a file object or a sample list')
        if sample_list is not None:
            self._samples = sample_list
        else:
            rows = csv.DictReader(mapping_file_object, delimiter='\t')
            self._samples = [row for row in rows]


        self.sample_ids = [x['#SampleID'] for x in self._samples]
        self._samples_by_id = {}
        for id_, sample in zip(self.sample_ids, self._samples):
            self._samples_by_id[id_] = sample


    def get_samples(self, column=None, values=None, unique=None):
        if values == '*':
            values = _AllTrue()

        if column is not None and values is not None:
            filtered_samples = []
            if unique is None:
                for sample in self._samples:
                    if sample[column] in values:
                        filtered_samples.append(sample)
            else:
                seen = set()
                for sample in self._samples:
                    if sample[column] in values and sample[unique] not in seen:
                        seen.add(sample[unique])
                        filtered_samples.append(sample)

            return filtered_samples
        return self._samples

    def get_sample(self, sampleID):
        if sampleID in self._samples_by_id:
            return self._samples_by_id[sampleID]
