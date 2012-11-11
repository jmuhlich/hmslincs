#!/bin/bash

set -e

[[ -n $VIRTUAL_ENV ]] && source $VIRTUAL_ENV/bin/activate

JOIN=${JOIN:-join}
CUT=${CUT:-cut}
DATADIR0=data/scatterplots
DATADIR1=${DATADIR1:-/tmp}
KLUGE=$DATADIR1/col_1_3.tsv
EXECDIR=$( dirname $( dirname $0 ) )

cd $EXECDIR || false

$JOIN -o 0,1.2,2.2 -a1 -a2 -e nan -t$'\t' \
    <( $CUT -f 1,2 $DATADIR0/'data_HTM (all GF), mean_raw(1).txt' ) \
    <( $CUT -f 1,3 $DATADIR0/'data_HTM (GF)_foldchange.tsv' ) \
  > $KLUGE

$JOIN -t$'\t' \
    $KLUGE \
    <( $CUT -f 1,3,5,6,29,31,32 $DATADIR0/'data_Basal levels_raw.tsv' ) \
  > $DATADIR1/picks_for_basal.tsv

$JOIN -t$'\t' \
    $KLUGE \
    <( $CUT -f 1,2,4,5,7,12,13,17,22 $DATADIR0/'data_HTM (all GF), mean_foldchange.tsv' ) \
  > $DATADIR1/picks_for_responses.tsv

# effectively, a 3-way join
$JOIN -t$'\t' <( $JOIN -t$'\t' \
                   $KLUGE \
                   <( cut -f 1,12,22 $DATADIR0/'data_HTM (all GF), mean_foldchange.tsv' ) ) \
              <( cut -f 1,67,68,69,127,128,129 $DATADIR0/'data_HTM (GF)_foldchange.tsv' ) \
  > $DATADIR1/picks_for_slider.tsv

python src/do_scatterplots.py $DATADIR1/picks_for_basal.tsv
python src/do_scatterplots.py $DATADIR1/picks_for_responses.tsv
WITHLIMITS=1 OUTPUTDIR=django/responses/static/responses/img/slider \
  python src/do_scatterplots.py $DATADIR1/picks_for_slider.tsv