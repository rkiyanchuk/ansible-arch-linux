MIRROR=http://mirror.rackspace.com/archlinux/iso
VERSION=$(shell date +"%Y.%m").01
IMAGE=archlinux-${VERSION}-x86_64.iso

iso:
	curl -o ${IMAGE} ${MIRROR}/${VERSION}/${IMAGE}
	curl -o ${IMAGE}.sig ${MIRROR}/${VERSION}/${IMAGE}.sig
	gpg --auto-key-retrieve --verify ${IMAGE}.sig
