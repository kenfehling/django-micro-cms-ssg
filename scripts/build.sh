SITE=$1
PUBLIC_ROOT=$2
BASE_BUILD_DIR=$3
OUTPUT_DIR=$BASE_BUILD_DIR/${SITE}

SITE=$SITE PUBLIC_ROOT=$PUBLIC_ROOT \
./manage.py distill-local \
    --exclude-staticfiles \
    --force \
    ${OUTPUT_DIR}
mkdir -p ${OUTPUT_DIR}/${PUBLIC_ROOT}/static
cp -r static/${SITE} ${OUTPUT_DIR}/${PUBLIC_ROOT}/static/${SITE}
cp -r static/cache ${OUTPUT_DIR}/${PUBLIC_ROOT}/static/cache
