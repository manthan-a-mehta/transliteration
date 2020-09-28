#!/usr/bin/env bash

POOL=1
RANK='0 '
PORT=19000


DATASET=$1'-'$2    # Add Language Folder here
RAW_PATH=${DATA_PATH}'/raw'/${DATASET}
PROCESSED_PATH=${DATA_PATH}'/processed'/${DATASET}
MODEL_PATH=${DATA_PATH}'/models'/${DATASET}
LOG_PATH=${DATA_PATH}/logs

cp ${ONMT_PATH}/tools/embeddings_to_torch.py ${ONMT_PATH}/embeddings_to_torch.py
mkdir -p ${LOG_PATH}

mkdir -p ${PROCESSED_PATH}

SRC_CODE=$1 # Change Source Language code
SRC=${RAW_PATH}'/raw.'${SRC_CODE}   # Change Source Language file name

TRG_CODE=$2 # Change Target Language code
TRG=${RAW_PATH}'/raw.'${TRG_CODE}   # Change Target Language file name

INPUT_FILE=${PROCESSED_PATH}/${SRC_CODE}'-'${TRG_CODE}'.syl'
OUTPUT_FILE=${PROCESSED_PATH}/${SRC_CODE}'-'${TRG_CODE}'.align'
LOG_FILE=${LOG_PATH}/${SRC_CODE}'-en'

if [[ -f ${SRC}  && -f ${TRG} ]]
then
    printf "Pre-processing..."
    if [[ -f ${INPUT_FILE} ]]
    then
        printf "\n${INPUT_FILE} already exists.Skipping.\n"
    else
        python ${CODE_PATH}/preProcessing.py \
            -src_lang ${SRC_CODE} \
            -src ${SRC} \
            -trg_lang ${TRG_CODE} \
            -trg ${TRG} \
            -out ${INPUT_FILE} \
            -char \
            > ${LOG_FILE}.log

        printf "Done.\n"
    fi
    printf "Starting m2m-aligner..."
    if [[ -f ${OUTPUT_FILE} ]]
    then
        printf "\n${OUTPUT_FILE} already exists.Skipping.\n"
    else
        ${M2M_PATH}/m2m-aligner \
            --sepChar ' ' \
            --sepInChar ' ' \
            -i ${INPUT_FILE} \
            -o ${OUTPUT_FILE} \
            >> ${LOG_FILE}.log

        printf "\nOperation complete. File saved at ${OUTPUT_FILE}\n"
    fi
    printf "Starting data splitter..."
    if [[ -f ${PROCESSED_PATH}/${SRC_CODE}'-train.txt' ]]
    then
        printf "\nAlready splitted!\n"
    else
        python ${CODE_PATH}/utils/splitter.py \
            ${OUTPUT_FILE} \
            ${PROCESSED_PATH}/${SRC_CODE}'-train.txt' \
            ${PROCESSED_PATH}/${TRG_CODE}'-train.txt' \
            ${PROCESSED_PATH}/${SRC_CODE}'-valid.txt' \
            ${PROCESSED_PATH}/${TRG_CODE}'-valid.txt' \
            ${PROCESSED_PATH}/${SRC_CODE}'-test.txt' \
            ${PROCESSED_PATH}/${TRG_CODE}'-test.txt' \
            >> ${LOG_FILE}.log

        printf "Done.\n"
    fi
else
    printf "Input file(s) not found!!\n"
fi

mkdir -p ${MODEL_PATH}

python ${ONMT_PATH}/preprocess.py \
    -train_src ${PROCESSED_PATH}/${SRC_CODE}-train.txt \
    -train_tgt ${PROCESSED_PATH}/${TRG_CODE}-train.txt \
    -valid_src ${PROCESSED_PATH}/${SRC_CODE}-valid.txt \
    -valid_tgt ${PROCESSED_PATH}/${TRG_CODE}-valid.txt \
    -save_data ${PROCESSED_PATH}/data \
    >> ${LOG_FILE}.log

parallelCode () {
    local rnn=$1
    local layer=$2
    local lr=$3
    local vs=$4
    local port=$5
    local log=${6}_${rnn}_${layer}_${lr}_${vs}.log
    local ts=50000

#    local enc_emb=$7
#    local dec_emb=$8


    model_name=${MODEL_PATH}/${DATASET}_${rnn}_${layer}_${lr}_${vs}

    python ${ONMT_PATH}/train.py \
        -data ${PROCESSED_PATH}/data \
        -save_model ${model_name} \
        -world_size ${POOL} \
        -gpu_ranks ${RANK} \
        -rnn_size ${rnn} \
        -word_vec_size ${vs} \
        -layers ${layer} \
        -optim adam \
        -learning_rate ${lr} \
        -train_step ${ts} \
        -encoder_type transformer \
        -master_port ${port} \
        > ${log}
#        -pre_word_vecs_enc ${enc_emb} \
#        -pre_word_vecs_dec ${dec_emb} \
#        > ${log}

    python ${ONMT_PATH}/translate.py \
        -model ${model_name}_step_${ts}.pt \
        -src ${PROCESSED_PATH}/${SRC_CODE}-test.txt \
        -output ${MODEL_PATH}/${DATASET}_${rnn}_${layer}_${lr}_${vs}_preds.txt \
        -replace_unk \
        >> ${log}

    python ${CODE_PATH}/utils/evaluate.py \
        acc \
        ${PROCESSED_PATH}/${TRG_CODE}-test.txt \
        ${MODEL_PATH}/${DATASET}_${rnn}_${layer}_${lr}_${vs}_preds.txt \
        True \
        >> ${log}
}

declare -a rnn=(128 256)
declare -a layer=(2 3)
declare -a lr=(1e-2 1e-3)
declare -a vs=(100 200 300)

#rnn=128
#layer=2
#lr=1e-3
#vs=100

## To train embeddings, uncomment this section
#for i in ${vs[@]}
#do
#    if [[ -f  ${PROCESSED_PATH}/${SRC_CODE}_${l}.emb ]]
#    then
#        printf "\nEmbeddings found!\n"
#    else
#        python ${CODE_PATH}/utils/generateEmbeddings.py \
#            ${OUTPUT_FILE} \
#            ${i}  \
#            ${PROCESSED_PATH}/${SRC_CODE}_${i}.emb \
#            ${PROCESSED_PATH}/${TRG_CODE}_${i}.emb \
#            >> ${LOG_FILE}.log
#        printf "Done.\n"
#    fi
#
#    python ${ONMT_PATH}/embeddings_to_torch.py \
#        -dict_file ${PROCESSED_PATH}/data.vocab.pt \
#        -emb_file_enc  ${PROCESSED_PATH}/${SRC_CODE}_${i}.emb \
#        -emb_file_dec ${PROCESSED_PATH}/${TRG_CODE}_${i}.emb \
#        -type 'word2vec' \
#        -output_file ${PROCESSED_PATH}/embeddings_${i} >> ${LOG_FILE}.log
#
#done

for i in ${rnn[@]}
do
    for j in ${layer[@]}
    do
        for k in ${lr[@]}
        do
            for l in ${vs[@]}
            do
                PORT=$(( $PORT + 10))
                parallelCode ${i} ${j} ${k} ${l} ${PORT} ${LOG_FILE} &  # ${PROCESSED_PATH}/embeddings_${l}.enc.pt  ${PROCESSED_PATH}/embeddings_${l}.dec.pt &
            done
        done
        wait
    done
done
