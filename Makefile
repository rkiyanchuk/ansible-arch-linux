VERSION=$(shell date +"%Y.%m").01
IMAGE=archlinux-${VERSION}-x86_64.iso

iso:
	curl -o ${IMAGE} http://mirror.rackspace.com/archlinux/iso/${VERSION}/${IMAGE}
	curl -o ${IMAGE}.sig https://www.archlinux.org/iso/${VERSION}/${IMAGE}.sig
	gpg --auto-key-retrieve --verify ${IMAGE}.sig
