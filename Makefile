VERSION=$(shell date +"%Y.%m").01
IMAGE=archlinux-${VERSION}-dual.iso

iso:
	wget http://mirror.rackspace.com/archlinux/iso/${VERSION}/${IMAGE} -O ${IMAGE}
	wget https://www.archlinux.org/iso/${VERSION}/${IMAGE}.sig -O ${IMAGE}.sig
	gpg --keyserver-options auto-key-retrieve --verify ${IMAGE}.sig || rm ${IMAGE}
