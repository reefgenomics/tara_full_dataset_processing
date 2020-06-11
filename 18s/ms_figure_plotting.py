"""
Script for plotting up the PCoAs of the distance plots and plotting up the line
graphs that show how the mantel tests change in reaction to the line graphs.

In general the order of these plots will be quite important as they are dependent on each other.
Preceeding plots will define proceeding as we will learn parameters from one that will be used in the
next. This narative should be written into the figure legends.

List of the plots that we want

PCoA plots:
1 - PCoA using the sequences as they are (i.e. with the most abundant sequences in place.)
2 - PCoA using with the majority sequences removed (but with the secondary samples still in place).
3 - PCOA using with the majority seuqences and secondary samples removed. This should likely be
plotted using the parameters inferred from the line plots.



Line plots:
1 - three row plot
Three rows to this plot that correspond to the three 'approaches' of the paper.
A - In the first row we will plot normalisation abundance against the persons correlation.
We can annotate individual point to show significance of the results. We should also likely annotate the
number of samples that are being compared.
As lines we will have each of the species, distance method and SNP w/wo = 2x2x2 = 8.
We also want to see the effect of normalisation method, but perhaps we will plot this in a separate plot.
We also want to plot the same but for minimum distinct seqs. This will probably have to go in a separate plot.

B - The second row will be similar to the first but looking at samples_at_least_threshold. So this will
be on the X.

C - The third row will again be similar format to the 2 rows above but looking at most_abund_seq_cutoff.

For rows B and C we will hold constant values according to the results of A.

As such. Let's start with the first row (A).

"""

from base_18s import EighteenSBase
import os
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt

class MSPlots(EighteenSBase):
    def __init__(self):
        super().__init__()

    def plot_three_row(self):
        """
        The three row plot.
        """
        tr = ThreeRow(parent=self)
        tr.plot()

class ThreeRow:
    def __init__(self, parent):
        self.parent = parent
        self.genera = ['Pocillopora', 'Porites']
        # Let's start with the first plot quick and dirty and then we can add the others
        # and refactorize.
        self.fig, self.ax = plt.subplots(3,3, figsize=(5,5))
        # plt.savefig(os.path.join(self.parent.eighteens_dir, 'temp_fig.png'), dpi=300)
        self.line_style_dict = {'rai':'-', 'pwr':'--', 'braycurtis':'-', 'unifrac':'--', True:'-', False:'--'}
        self.line_color_dict = {'Pocillopora':'black', 'Porites':'grey'}

        
    def _plot_line_first_row(self, ax, genus, linestyle, color, normalisation_method='rai', distance_method='braycurtis', snp_only=False):
        # We want to find all files in the 18s output directory where:
        # genus == g
        results_dict = {}
        for result_file in [_ for _ in os.listdir(self.parent.output_dir_18s) if _.endswith('_mantel_result.txt')]:
            if result_file.startswith(f'{genus}_True_True_True_False_biallelic_{distance_method}_dist'):
                # inbetween these to conditions is the nomalisation_abundance
                if result_file.endswith(f'{normalisation_method}_{snp_only}_0_0_3_mantel_result.txt'):
                # if result_file.endswith(f'{n_m}_False_0_0_3_mantel_result.txt'):
                    # Then this is a set of points for plotting
                    # We want to get them in order
                    # the normalisation depth is the 8th item
                    # create a dict of normalisation depth to tuple.
                    # Where tuple is p_value and correlation coef.
                    with open(os.path.join(self.parent.output_dir_18s, result_file), 'r') as f:
                            (cor_coef, p_val) = [float(_) for _ in f.read().rstrip().lstrip().split('\t')]
                    norm_value = int(result_file.split('_')[8])
                    if norm_value not in results_dict:
                        results_dict[norm_value] = (cor_coef, p_val)
                    else:
                        raise RuntimeError('Dict already contains norm_value')
        
        # Here we have a results dict ready for plotting for one of the g/m/snp combos.
        # For starters plot up the line plain. Then changge line characters. then annotate with p value
        sorted_norm = sorted(results_dict.keys())
        ax.plot(
            sorted_norm, 
            [results_dict[_][0] for _ in sorted_norm],
            label=f'{genus}_{normalisation_method}_{distance_method}_{snp_only}', color=color, linestyle=linestyle, linewidth=0.5)
        # ax.legend(fontsize=2, loc='best')
        foo = 'bar'

    def _plot_line_second_row(self, ax, genus, linestyle, color, normalisation_abundance, normalisation_method='pwr', distance_method='braycurtis', snp_only=False):
        # We want to find all files in the 18s output directory where:
        # genus == g
        results_dict = {}
        for result_file in [_ for _ in os.listdir(self.parent.output_dir_18s) if _.endswith('_mantel_result.txt')]:
            if result_file.startswith(f'{genus}_True_True_True_False_biallelic_{distance_method}_dist_{normalisation_abundance}_{normalisation_method}_{snp_only}'):
                # inbetween these to conditions is the nomalisation_abundance
                if result_file.endswith(f'_0_3_mantel_result.txt'):
                    # Then this is a set of points for plotting
                    # We want to get them in order
                    # the samples_at_least_threshold is the 8th item
                    # create a dict of samples_at_least_threshold to tuple.
                    # Where tuple is p_value and correlation coef.
                    with open(os.path.join(self.parent.output_dir_18s, result_file), 'r') as f:
                            (cor_coef, p_val) = [float(_) for _ in f.read().rstrip().lstrip().split('\t')]
                    norm_value = float(result_file.split('_')[11])
                    if norm_value not in results_dict:
                        results_dict[norm_value] = (cor_coef, p_val)
                    else:
                        if norm_value != 0:
                            raise RuntimeError('Dict already contains norm_value')
                        else:
                            # We have _0_ and _0.0_ because of how the distances were calculated.
                            # They are actually different but both give p_val >> 0.05 and coef ~ 0.
                            pass
        
        # Here we have a results dict ready for plotting for one of the g/m/snp combos.
        # For starters plot up the line plain. Then changge line characters. then annotate with p value
        sorted_norm = sorted(results_dict.keys())
        # ax2=ax.twinx()
        ax.plot(
            sorted_norm, 
            [results_dict[_][0] for _ in sorted_norm],
            label=f'{genus}_{normalisation_method}_{distance_method}_{snp_only}', 
            color=color,
            linestyle=linestyle,
            linewidth=0.5)
        # ax.legend(fontsize=2, loc='best')
        foo = 'bar'

    def _plot_line_third_row(self, ax, genus, linestyle, color, normalisation_abundance, normalisation_method='pwr', distance_method='braycurtis', snp_only=False):
        
        results_dict = {}
        for result_file in [_ for _ in os.listdir(self.parent.output_dir_18s) if _.endswith('_mantel_result.txt')]:
            if result_file.startswith(f'{genus}_True_True_True_False_biallelic_{distance_method}_dist_{normalisation_abundance}_{normalisation_method}_{snp_only}_0_'):
                # inbetween these to conditions is the nomalisation_abundance
                if result_file.endswith(f'_3_mantel_result.txt'):
                    # Then this is a set of points for plotting
                    # We want to get them in order
                    # the samples_at_least_threshold is the 8th item
                    # create a dict of samples_at_least_threshold to tuple.
                    # Where tuple is p_value and correlation coef.
                    with open(os.path.join(self.parent.output_dir_18s, result_file), 'r') as f:
                            (cor_coef, p_val) = [float(_) for _ in f.read().rstrip().lstrip().split('\t')]
                    norm_value = int(result_file.split('_')[12])
                    if norm_value not in results_dict:
                        results_dict[norm_value] = (cor_coef, p_val)
                    else:
                        if norm_value != 0:
                            raise RuntimeError('Dict already contains norm_value')
                        else:
                            # We have _0_ and _0.0_ because of how the distances were calculated.
                            # They are actually different but both give p_val >> 0.05 and coef ~ 0.
                            pass
        
        # Here we have a results dict ready for plotting for one of the g/m/snp combos.
        # For starters plot up the line plain. Then changge line characters. then annotate with p value
        sorted_norm = sorted(results_dict.keys())
        # ax2=ax.twinx()
        ax.plot(
            sorted_norm, 
            [results_dict[_][0] for _ in sorted_norm],
            label=f'{genus}_{normalisation_method}_{distance_method}_{snp_only}', 
            color=color,
            linestyle=linestyle,
            linewidth=0.5)
        # ax.legend(fontsize=2, loc='best')
        foo = 'bar'


    def plot(self):
        """
        For the record, the results string format:
        self.unique_string = f'{self.genus}_{self.remove_maj_seq}_{self.exclude_secondary_seq_samples}_' \
        f'{self.exclude_no_use_samples}_{self.use_replicates}_' \
        f'{snp_distance_type}_{self.dist_method_18S}_' \
        f'{self.approach}_{self.normalisation_abundance}_{self.normalisation_method}_' \
        f'{self.only_snp_samples}_{self.samples_at_least_threshold}_' \
        f'{self.most_abund_seq_cutoff}_{self.min_num_distinct_seqs_per_sample}'
        self.result_path = os.path.join('/home/humebc/projects/tara/tara_full_dataset_processing/18s/output', f'{self.unique_string}_mantel_result.txt')
        """
        
        self._plot_first_row()
        self._plot_second_row()
        self._plot_third_row()
        plt.savefig(os.path.join(self.parent.eighteens_dir, 'temp_fig.png'), dpi=1200)
        self.foo = 'bar'

    def _plot_third_row(self):
        # RESULTS This shows us that once again, the effect is very genus dependent
        # For Porites, using this threshold argubly has some benefit to a small degree but questionable.
        # However for Pocillopora it appears to have little or no effect.
        # TODO test some combinations of these two factors to see if we find some surprising results.
        # for g in self.genera:
        #     for m in ['unifrac', 'braycurtis']:
        #         if m == 'unifrac':
        #             norm_abund = 1000
        #         else:
        #             norm_abund = 10000
        #         self._plot_line_third_row(ax=self.ax[2][0], genus=g, color=self.line_color_dict[g], normalisation_abundance=norm_abund, linestyle=self.line_style_dict[m], normalisation_method='pwr', distance_method=m, snp_only=False)
            
        # We can additionally now in theory work on the corsses of the samples_at_least_threshold and the 
        # most_abund_seq_cutoff.
        # We will need to look at a countor for each variable combination I guess
        # so one for each of the genera and dist methods
        for g in self.genera:
            for m in ['unifrac', 'braycurtis']:
                if m == 'unifrac':
                    norm_abund = 1000
                else:
                    norm_abund = 10000
                self._plot_countour(ax=self.ax[2][0], genus=g, normalisation_abundance=norm_abund, normalisation_method='pwr', distance_method=m, snp_only=False)

    def _plot_countour(self, ax, genus, distance_method, normalisation_abundance, normalisation_method='pwr', snp_only=False):
        # Plot a contour plot where we have samples_at_least_threshold on the x and most_abund_seq_cutoff on the y
        # and then the coef on the z.
        x_samples_at_least_threshold = []
        y_most_abund_seq_cutoff = []
        z_coef = []
        z_p_val = []
        for result_file in [_ for _ in os.listdir(self.parent.output_dir_18s) if _.endswith('_mantel_result.txt')]:
            if result_file.startswith(f'{genus}_True_True_True_False_biallelic_{distance_method}_dist_{normalisation_abundance}_{normalisation_method}_{snp_only}_'):
                # inbetween these to conditions is the nomalisation_abundance
                if result_file.endswith(f'_3_mantel_result.txt'):
                    # Then this is a set of points for plotting
                    
                    with open(os.path.join(self.parent.output_dir_18s, result_file), 'r') as f:
                            (cor_coef, p_val) = [float(_) for _ in f.read().rstrip().lstrip().split('\t')]
                    samples_at_least_threshold = float(result_file.split('_')[11])
                    most_abund_seq_cutoff = int(result_file.split('_')[12])
                    x_samples_at_least_threshold.append(samples_at_least_threshold)
                    y_most_abund_seq_cutoff.append(most_abund_seq_cutoff)
                    z_coef.append(cor_coef)
                    z_p_val.append(p_val)
                    
        df = pd.DataFrame(columns=[int(_) for _ in set(y_most_abund_seq_cutoff)], index=list(set(x_samples_at_least_threshold)))
        
        for x,y,z in zip(x_samples_at_least_threshold, y_most_abund_seq_cutoff, z_coef):
            df.at[x,y] = z
        
        ax.contourf(x=list(df.index), y=list(df), z=df.to_numpy(dtype=float))
        foo = 'bar'


    def _plot_second_row(self):
        # RESULT This shows us that the effect of the samples_at_least_threshold is dependent on the genus
        # being investigated. For Porites it has a negative effect.
        # However, for Pocillopora, it hav a positive effect.
        # The distance method i.e. unifrac or braycurtis has little effect.
        for g in self.genera:
            for m in ['unifrac', 'braycurtis']:
                if m == 'unifrac':
                    norm_abund = 1000
                else:
                    norm_abund = 10000
                self._plot_line_second_row(ax=self.ax[1][0], genus=g, color=self.line_color_dict[g], normalisation_abundance=norm_abund, linestyle=self.line_style_dict[m], normalisation_method='pwr', distance_method=m, snp_only=False)

    def _plot_first_row(self):
        # RESULT This plot shows us that UniFrac is bascially going mental
        # The results basically look random.
        # RESULT For Bray curtis we see a slight improvement
        # up to about the 10 000 point. So I think this looks like a sensible cutoff to work with.
        # RESULT The pwr vs rai makes very little difference so I would say that we can work with either
        # The only difference being that one comes from below and one from above. We can work with either moving forwards
        # RESULT For the with and without SNP samples there is almost no difference. I think we can put a very positive
        # spin on this. This means that the additional samples are not effecting how they are being resolved.
        # TODO plot out an example pcoa plot of this to show that the poosition of samples does not change much
        # actually not sure that this is possible but maybe investigate.
        # As for displaying these facts, Porites and Pocillopora separate nicely as there appears to be a far stronger
        # correlation between porties (almost double). This may be due to the lack of structuring in Pocillopora.
        # This means that it works well to have both genera in each of the plots. I think we can do a plot for
        # distance method, normalisation method and for only_smp_samples.
        # TODO given that the unifrac basically doesn't work with the 0 cutoff, there's not much point testing it using
        # this value. So Rather, we should test it using one of the cutoffs that will be determined in row 2 I guess.
        for g in self.genera:
            for m in ['unifrac', 'braycurtis']:
                self._plot_line_first_row(ax=self.ax[0][0], genus=g, color=self.line_color_dict[g], linestyle=self.line_style_dict[m], normalisation_method='rai', distance_method=m, snp_only=False)

            for n_m in ['pwr', 'rai']:
                self._plot_line_first_row(ax=self.ax[0][1], genus=g, color=self.line_color_dict[g], linestyle=self.line_style_dict[n_m],normalisation_method=n_m, distance_method='braycurtis', snp_only=False)

            # NB the only way that having SNP samples can make a difference is during the Unifrac and Unifrac isn't really working here
            # Otherwise, if you think about it, exactly the same pairwise comparisons are going to be considered for the braycurtis and
            # then we're already stripping down to only the SNP comparison in the mantel.
            # We want to be looking at the SNP/noSNP for the cluster assignment.
            # for only_snp_samples in [True, False]: # We are computing this now.
            #     self._plot_line_first_row(ax=self.ax[0][2], genus=g, color=self.line_color_dict[g], linestyle=self.line_style_dict[only_snp_samples],normalisation_method='rai', distance_method='unifrac', snp_only=only_snp_samples)
        
        self.ax[0][0].set_title('dist_method')
        self.ax[0][1].set_title('norm_method')
        # self.ax[0][2].set_title('snp_samples_only')

MSPlots().plot_three_row()