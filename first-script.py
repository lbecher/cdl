import os
import sys
import platform
import getpass
import textwrap
import subprocess

bash_profile = '''
exec env -i HOME=$HOME TERM=$TERM PS1=\'\\u:\\w\\$ \' /bin/bash
'''

bashrc = '''
set +h
umask 022
LFS=/mnt/{}
LC_ALL=POSIX
LFS_TGT=$(uname -m)-{}-linux-gnu
PATH=/usr/bin
if [ ! -L /bin ]; then PATH=/bin:$PATH; fi
PATH=$LFS/tools/bin:$PATH
export LFS LC_ALL LFS_TGT PATH
'''

kernels = [
'''
https://www.kernel.org/pub/linux/utils/net/iproute2/iproute2-5.4.0.tar.xz
https://www.kernel.org/pub/linux/kernel/v5.x/linux-5.4.86.tar.xz
''',
'''
https://www.kernel.org/pub/linux/utils/net/iproute2/iproute2-5.8.0.tar.xz
https://www.kernel.org/pub/linux/kernel/v5.x/linux-5.8.3.tar.xz
''',
'''
https://www.kernel.org/pub/linux/utils/net/iproute2/iproute2-5.10.0.tar.xz
https://www.kernel.org/pub/linux/kernel/v5.x/linux-5.10.4.tar.xz
''',
]

text_editors = [
'''
https://www.nano-editor.org/dist/v5/nano-5.4.tar.xz
''',
'''
http://anduin.linuxfromscratch.org/LFS/vim-8.2.1361.tar.gz
''',
]

lfs_wget_list = '''
http://download.savannah.gnu.org/releases/acl/acl-2.2.53.tar.gz
http://download.savannah.gnu.org/releases/attr/attr-2.4.48.tar.gz
http://ftp.gnu.org/gnu/autoconf/autoconf-2.69.tar.xz
http://ftp.gnu.org/gnu/automake/automake-1.16.2.tar.xz
http://ftp.gnu.org/gnu/bash/bash-5.0.tar.gz
https://github.com/gavinhoward/bc/releases/download/3.1.5/bc-3.1.5.tar.xz
http://ftp.gnu.org/gnu/binutils/binutils-2.35.tar.xz
http://ftp.gnu.org/gnu/bison/bison-3.7.1.tar.xz
https://www.sourceware.org/pub/bzip2/bzip2-1.0.8.tar.gz
https://github.com/libcheck/check/releases/download/0.15.2/check-0.15.2.tar.gz
http://ftp.gnu.org/gnu/coreutils/coreutils-8.32.tar.xz
https://dbus.freedesktop.org/releases/dbus/dbus-1.12.20.tar.gz
http://ftp.gnu.org/gnu/dejagnu/dejagnu-1.6.2.tar.gz
http://ftp.gnu.org/gnu/diffutils/diffutils-3.7.tar.xz
https://downloads.sourceforge.net/project/e2fsprogs/e2fsprogs/v1.45.6/e2fsprogs-1.45.6.tar.gz
https://sourceware.org/ftp/elfutils/0.180/elfutils-0.180.tar.bz2
https://dev.gentoo.org/~blueness/eudev/eudev-3.2.9.tar.gz
https://prdownloads.sourceforge.net/expat/expat-2.2.9.tar.xz
https://prdownloads.sourceforge.net/expect/expect5.45.4.tar.gz
ftp://ftp.astron.com/pub/file/file-5.39.tar.gz
http://ftp.gnu.org/gnu/findutils/findutils-4.7.0.tar.xz
https://github.com/westes/flex/releases/download/v2.6.4/flex-2.6.4.tar.gz
http://ftp.gnu.org/gnu/gawk/gawk-5.1.0.tar.xz
http://ftp.gnu.org/gnu/gcc/gcc-10.2.0/gcc-10.2.0.tar.xz
http://ftp.gnu.org/gnu/gdbm/gdbm-1.18.1.tar.gz
http://ftp.gnu.org/gnu/gettext/gettext-0.21.tar.xz
http://ftp.gnu.org/gnu/glibc/glibc-2.32.tar.xz
http://ftp.gnu.org/gnu/gmp/gmp-6.2.0.tar.xz
http://ftp.gnu.org/gnu/gperf/gperf-3.1.tar.gz
http://ftp.gnu.org/gnu/grep/grep-3.4.tar.xz
http://ftp.gnu.org/gnu/groff/groff-1.22.4.tar.gz
https://ftp.gnu.org/gnu/grub/grub-2.04.tar.xz
http://ftp.gnu.org/gnu/gzip/gzip-1.10.tar.xz
https://github.com/Mic92/iana-etc/releases/download/20200821/iana-etc-20200821.tar.gz
http://ftp.gnu.org/gnu/inetutils/inetutils-1.9.4.tar.xz
https://launchpad.net/intltool/trunk/0.51.0/+download/intltool-0.51.0.tar.gz
https://www.kernel.org/pub/linux/utils/kbd/kbd-2.3.0.tar.xz
https://www.kernel.org/pub/linux/utils/kernel/kmod/kmod-27.tar.xz
http://www.greenwoodsoftware.com/less/less-551.tar.gz
http://www.linuxfromscratch.org/lfs/downloads/10.0/lfs-bootscripts-20200818.tar.xz
https://www.kernel.org/pub/linux/libs/security/linux-privs/libcap2/libcap-2.42.tar.xz
ftp://sourceware.org/pub/libffi/libffi-3.3.tar.gz
http://download.savannah.gnu.org/releases/libpipeline/libpipeline-1.5.3.tar.gz
http://ftp.gnu.org/gnu/libtool/libtool-2.4.6.tar.xz
http://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.xz
http://ftp.gnu.org/gnu/make/make-4.3.tar.gz
http://download.savannah.gnu.org/releases/man-db/man-db-2.9.3.tar.xz
https://www.kernel.org/pub/linux/docs/man-pages/man-pages-5.08.tar.xz
https://github.com/mesonbuild/meson/releases/download/0.55.0/meson-0.55.0.tar.gz
https://ftp.gnu.org/gnu/mpc/mpc-1.1.0.tar.gz
http://www.mpfr.org/mpfr-4.1.0/mpfr-4.1.0.tar.xz
http://ftp.gnu.org/gnu/ncurses/ncurses-6.2.tar.gz
https://github.com/ninja-build/ninja/archive/v1.10.0/ninja-1.10.0.tar.gz
https://www.openssl.org/source/openssl-1.1.1g.tar.gz
http://ftp.gnu.org/gnu/patch/patch-2.7.6.tar.xz
https://www.cpan.org/src/5.0/perl-5.32.0.tar.xz
https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz
https://sourceforge.net/projects/procps-ng/files/Production/procps-ng-3.3.16.tar.xz
https://sourceforge.net/projects/psmisc/files/psmisc/psmisc-23.3.tar.xz
https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tar.xz
https://www.python.org/ftp/python/doc/3.8.5/python-3.8.5-docs-html.tar.bz2
http://ftp.gnu.org/gnu/readline/readline-8.0.tar.gz
http://ftp.gnu.org/gnu/sed/sed-4.8.tar.xz
https://github.com/shadow-maint/shadow/releases/download/4.8.1/shadow-4.8.1.tar.xz
http://www.infodrom.org/projects/sysklogd/download/sysklogd-1.5.1.tar.gz
https://github.com/systemd/systemd/archive/v246/systemd-246.tar.gz
http://anduin.linuxfromscratch.org/LFS/systemd-man-pages-246.tar.xz
http://download.savannah.gnu.org/releases/sysvinit/sysvinit-2.97.tar.xz
http://ftp.gnu.org/gnu/tar/tar-1.32.tar.xz
https://downloads.sourceforge.net/tcl/tcl8.6.10-src.tar.gz
https://downloads.sourceforge.net/tcl/tcl8.6.10-html.tar.gz
http://ftp.gnu.org/gnu/texinfo/texinfo-6.7.tar.xz
https://www.iana.org/time-zones/repository/releases/tzdata2020a.tar.gz
http://anduin.linuxfromscratch.org/LFS/udev-lfs-20171102.tar.xz
https://www.kernel.org/pub/linux/utils/util-linux/v2.36/util-linux-2.36.tar.xz
https://cpan.metacpan.org/authors/id/T/TO/TODDR/XML-Parser-2.46.tar.gz
https://tukaani.org/xz/xz-5.2.5.tar.xz
https://zlib.net/zlib-1.2.11.tar.xz
https://github.com/facebook/zstd/releases/download/v1.4.5/zstd-1.4.5.tar.gz
http://www.linuxfromscratch.org/patches/lfs/10.0/bash-5.0-upstream_fixes-1.patch
http://www.linuxfromscratch.org/patches/lfs/10.0/bzip2-1.0.8-install_docs-1.patch
http://www.linuxfromscratch.org/patches/lfs/10.0/coreutils-8.32-i18n-1.patch
http://www.linuxfromscratch.org/patches/lfs/10.0/glibc-2.32-fhs-1.patch
http://www.linuxfromscratch.org/patches/lfs/10.0/kbd-2.3.0-backspace-1.patch
http://www.linuxfromscratch.org/patches/lfs/10.0/sysvinit-2.97-consolidated-1.patch
'''

def wprint(s):
    print('\n'.join(textwrap.wrap(s, width = os.get_terminal_size(0)[0], replace_whitespace = False)))


def winput(s):
    return input('\n'.join(textwrap.wrap(s, width = os.get_terminal_size(0)[0], drop_whitespace = False)))


def wgetpass(s):
    return getpass.getpass('\n'.join(textwrap.wrap(s, width = os.get_terminal_size(0)[0], drop_whitespace = False)))


def ask_to_continue():
    print('')
    choice = winput('Você deseja continuar? (Digite 1 para sim, ou qualquer outro caractere para não) ')
    if choice != '1':
        sys.exit()
    print('')


def check_system():
    if platform.system() != 'Linux':
        wprint('ERRO: Sistema não compatível. Este script é destinado para sistemas Linux.')
        sys.exit()


def check_architecture():
    if platform.machine() != 'x86_64':
        wprint('ERRO: Sistema não compatível. Este script é destinado para sistemas x86_64.')
        sys.exit()


def check_user():
    if getpass.getuser() != 'root':
        wprint('ERRO: Este script precisa ser executado pelo usuário root.')
        sys.exit()


def validate_character(character):
    if character in 'qwertyuiopasdfghjklzxcvbnm':
        return True
    else:
        return False


def prepare_ubuntu_host():
    os.system('apt update')
    os.system('apt update')
    os.system('apt upgrade -y')
    os.system('apt install -y sudo bash binutils bison bzip2 coreutils diffutils findutils gawk gcc grep gzip m4 make patch perl python3 sed tar texinfo xz-utils')
    os.system('ln -sf bash /bin/sh')


def add_user_and_group():
    wprint('Crie uma senha para ' + name + '.')
    password = wgetpass('Senha: ')
    confirmation_password = wgetpass('Confirme a senha: ')
    while password != confirmation_password or len(password) < 6:
        if password != confirmation_password:
            wprint('As senhas não combinam.')
        if len(password) < 6:
            wprint('Sua senha tem menos de seis caracteres.')
        wprint('Tente novamente.')
        password = wgetpass('Senha: ')
        confirmation_password = wgetpass('Confirme a senha: ')
    os.system('groupadd ' + name)
    os.system('useradd -s /bin/bash -g ' + name + ' -m -k /dev/null ' + name)
    os.system('echo "' + name + ':' + password + '" | chpasswd')


def format_partition():
    partition = winput('Insira uma partição para hospedar sua distribuição (ex: sda5 ou sdb1): ')
    print('')
    ls_return = subprocess.check_output('ls /dev/', shell = True)
    while not partition in ls_return.decode("utf-8"):
        wprint('Essa partição não existe no sistema hospedeiro. Tente novamente.')
        partition = winput('Insira uma partição para hospedar sua distribuição (ex: sda5 ou sdb1): ')
    os.system('mkfs -v -t ext4 /dev/' + partition)
    os.system('mkdir -pv /mnt/' + name)
    os.system('mount -v -t ext4 /dev/' + partition + ' /mnt/' + name)


def create_directory_structure():
    os.system('mkdir -pv /mnt/' + name + '/bin')
    os.system('mkdir -pv /mnt/' + name + '/etc')
    os.system('mkdir -pv /mnt/' + name + '/lib')
    os.system('mkdir -pv /mnt/' + name + '/sbin')
    os.system('mkdir -pv /mnt/' + name + '/usr')
    os.system('mkdir -pv /mnt/' + name + '/var')
    os.system('mkdir -pv /mnt/' + name + '/tools')
    os.system('mkdir -pv /mnt/' + name + '/sources')
    os.system('mkdir -pv /mnt/' + name + '/lib64')
    os.system('chown -v ' + name + ' /mnt/' + name + '/bin')
    os.system('chown -v ' + name + ' /mnt/' + name + '/etc')
    os.system('chown -v ' + name + ' /mnt/' + name + '/lib')
    os.system('chown -v ' + name + ' /mnt/' + name + '/sbin')
    os.system('chown -v ' + name + ' /mnt/' + name + '/usr')
    os.system('chown -v ' + name + ' /mnt/' + name + '/var')
    os.system('chown -v ' + name + ' /mnt/' + name + '/tools')
    os.system('chown -v ' + name + ' /mnt/' + name + '/sources')
    os.system('chown -v ' + name + ' /mnt/' + name + '/lib64')
    os.system('chmod -v a+wt /mnt/' + name + '/sources')


def download_packages():
    kernel_choice = -1
    while kernel_choice > 3 or kernel_choice < 1:
        wprint('Selecione a versão do kernel a ser baixada para sua distribuição:')
        wprint(' 1 - Linux Kernel 5.4.86 LTS')
        wprint(' 2 - Linux Kernel 5.8.0')
        wprint(' 3 - Linux Kernel 5.10.4')
        kernel_choice = int(winput('Digite o número da sua escolha: '))
        if kernel_choice > 3 or kernel_choice < 1:
            wprint('Essa opção não existe. Tente novamente.')
    text_editor_choice = -1
    while text_editor_choice > 2 or text_editor_choice < 1:
        wprint('Selecione o editor de texto a ser baixado para sua distribuição:')
        wprint(' 1 - Editor de texto Nano')
        wprint(' 2 - Editor de texto Vim')
        text_editor_choice = int(winput('Digite o número da sua escolha: '))
        if text_editor_choice > 2 or text_editor_choice < 1:
            wprint('Essa opção não existe. Tente novamente.')
    print('')
    open('/mnt/' + name + '/sources/wget-list', 'w').write(lfs_wget_list + text_editors[text_editor_choice - 1] + kernels[kernel_choice - 1])
    os.system('wget --input-file=/mnt/' + name + '/sources/wget-list --continue --directory-prefix=/mnt/' + name + '/sources')
    os.system('chown -v ' + name + ' /mnt/' + name + '/sources/*')
    os.system('chmod -v 644 /mnt/' + name + '/sources/*')


def configure_environment():
    os.system('[ ! -e /etc/bash.bashrc ] || mv -v /etc/bash.bashrc /etc/bash.bashrc.NOUSE')
    open('/home/' + name + '/.bash_profile', 'w').write(bash_profile)
    open('/home/' + name + '/.bashrc', 'w').write(bashrc.format(name, name))
    os.system('chown -v ' + name + ' /home/' + name + '/.bash_profile')
    os.system('chown -v ' + name + ' /home/' + name + '/.bashrc')
    os.system('chmod -v 664 /home/' + name + '/.bash_profile')
    os.system('chmod -v 664 /home/' + name + '/.bashrc')
    os.system('sudo -i -u ' + name + ' sh -c \'source ~/.bash_profile\'')


os.system('clear')

print('')
wprint('[Linux Distribution Builder]')
print('')
wprint('Este script pretende criar uma distribuição Linux, baseando-se no livro Linux From Scratch 10.0. Acesse o material em http://www.linuxfromscratch.org/ para ter uma noção mais aprofundada do que vem adiante.')
print('')
wprint('Script em execução: primeiro script.')
print('')
wprint('O que este script fará neste sistema (sistema hospedeiro):')
wprint(' - Criará um usuário;')
wprint(' - Criará um grupo de usuários;')
wprint(' - Instalará dependências;')
wprint(' - Alterará o link simbólico so bash;')
wprint(' - Formatará uma partição a ser especificada;')
wprint(' - Montará a partição em /mnt/<<<nome da distribuição>>>;')
wprint(' - Criará uma estrutura de diretórios na partição;')
wprint(' - Definirá o owner e as permissões dos diretórios;')
wprint(' - Baixará pacotes para compilação;')
wprint(' - Renomeará o arquivo /etc/bash.bashrc para /etc/bash.bashrc.NOUSE.')

ask_to_continue()

wprint('Verificando requisitos de execução...')
check_architecture()
check_system()
check_user()
wprint('Tudo certo até o momento.')
print('')

name = winput('Insira um nome para sua distribuição: ')

while not all(validate_character(c) for c in name):
    wprint('Não use letras maiúsculas, números, espaços ou caracteres especiais.')
    name = winput('Insira um nome para sua distribuição: ')

print('')
wprint('As dependências serão instaladas no sistema hospedeiro.')
ask_to_continue()
prepare_ubuntu_host() # substitua por outras distros futuramente

print('')
wprint('O usuário ' + name + ' e seu grupo, de mesmo nome, serão criados no sistema hospedeiro.')
ask_to_continue()
add_user_and_group()

print('')
wprint('A partição de hospedagem será formatada e configurada.')
ask_to_continue()
format_partition()

print('')
wprint('A estrutura de diretórios será criada na partição escolhida.')
ask_to_continue()
create_directory_structure()

print('')
wprint('Os pacotes serão baixados com base no wget-list do Linux From Scratch.')
ask_to_continue()
download_packages()

print('')
wprint('O ambiente do usuário ' + name + ' será configurado. O Script terminará no terminal de ' + name + '.')
ask_to_continue()
configure_environment()
