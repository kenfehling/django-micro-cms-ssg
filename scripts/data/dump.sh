./manage.py dumpdata \
    --exclude admin \
    --exclude auth \
    --exclude sessions \
    --exclude contenttypes \
    --exclude thumbnail \
    --format yaml \
    --output dump.yaml
