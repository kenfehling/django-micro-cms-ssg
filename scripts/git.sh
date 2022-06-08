mkdir -p ~/.ssh
ssh-keygen -F github.com || ssh-keyscan github.com >>~/.ssh/known_hosts

SITE=$1
GIT_REPO=$2
PUBLIC_ROOT=$3
BASE_BUILD_DIR=$4
BUILD_DIR=$BASE_BUILD_DIR/${SITE}/${PUBLIC_ROOT}
CLONE_DIR=/tmp/${SITE}_clone

rm -rf ${CLONE_DIR}
git clone ${GIT_REPO} ${CLONE_DIR}
cp -r ${BUILD_DIR}/* ${CLONE_DIR}
cd ${CLONE_DIR} || exit
git add --all
git commit -m "build"
git push -u origin main
