import os
import os.path
import sys
import platform
import getpass
import textwrap

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


def mount_partition():
    partition = winput('Insira a partição onde sua distribuição está hospedada (ex: sda5 ou sdb1): ')
    print('')
    while not os.path.exists('/dev/' + partition):
        wprint('Essa partição não existe no sistema hospedeiro. Tente novamente.')
        partition = winput('Insira uma partição para hospedar sua distribuição (ex: sda5 ou sdb1): ')
    os.system('mount -v -t ext4 /dev/' + partition + ' /mnt/' + name)


def compile_host_binutils():
    os.chdir('/mnt/' + name + '/sources')
    os.system('sudo -i -u ' + name + ' sh -c \'tar -xf binutils-2.35.tar.xz\'')
    os.system('sudo -i -u ' + name + ' sh -c \'mkdir -v /mnt/' + name + '/sources/binutils-2.35/build\'')
    os.chdir('/mnt/' + name + '/sources/binutils-2.35/build')
    os.system('sudo -i -u ' + name + ' sh -c \'time ../configure --prefix=$LFS/tools --with-sysroot=$LFS --target=$LFS_TGT --disable-nls --disable-werror\'')
    os.system('sudo -i -u ' + name + ' sh -c \'time make\'')
    os.system('sudo -i -u ' + name + ' sh -c \'time make install\'')


def compile_host_gcc():
    os.chdir('/mnt/' + name + '/sources')
    os.system('sudo -i -u ' + name + ' sh -c \'tar -xf gcc-10.2.0.tar.xz\'')
    os.chdir('/mnt/' + name + '/sources/gcc-10.2.0')
    os.system('sudo -i -u ' + name + ' sh -c \'tar -xf ../mpfr-4.1.0.tar.xz && mv -v mpfr-4.1.0 mpfr && tar -xf ../gmp-6.2.0.tar.xz && mv -v gmp-6.2.0 gmp && tar -xf ../mpc-1.1.0.tar.gz && mv -v mpc-1.1.0 mpc && sed -e \'/m64=/s/lib64/lib/\' -i.orig gcc/config/i386/t-linux64\'')
    os.system('sudo -i -u ' + name + ' sh -c \'mkdir -v /mnt/' + name + '/sources/gcc-10.2.0/build\'')
    os.chdir('/mnt/' + name + '/sources/gcc-10.2.0/build')
    os.system('sudo -i -u ' + name + ' sh -c \'time ../configure --target=$LFS_TGT --prefix=$LFS/tools --with-glibc-version=2.11 --with-sysroot=$LFS --with-newlib --without-headers --enable-initfini-array --disable-nls --disable-shared --disable-multilib --disable-decimal-float --disable-threads --disable-libatomic --disable-libgomp --disable-libquadmath --disable-libssp --disable-libvtv --disable-libstdcxx --enable-languages=c,c++\'')
    os.system('sudo -i -u ' + name + ' sh -c \'time make\'')
    os.system('sudo -i -u ' + name + ' sh -c \'time make install\'')
    os.chdir('/mnt/' + name + '/sources/gcc-10.2.0')
    os.system('sudo -i -u ' + name + ' sh -c \'cat gcc/limitx.h gcc/glimits.h gcc/limity.h > `dirname $($LFS_TGT-gcc -print-libgcc-file-name)`/install-tools/include/limits.h\'')


os.system('clear')

print('')
wprint('[Linux Distribution Builder]')
print('')
wprint('Este script pretende criar uma distribuição Linux, baseando-se no livro Linux From Scratch 10.0. Acesse o material em http://www.linuxfromscratch.org/ para ter uma noção mais aprofundada do que vem adiante.')
print('')
wprint('Script em execução: segundo script.')
print('')
wprint('O que este script fará neste sistema (sistema hospedeiro):')
wprint(' - Compilará o pacote Binutils;')
wprint(' - Compilará o pacote GCC;')

ask_to_continue()

wprint('Verificando requisitos de execução...')
check_architecture()
check_system()
check_user()
wprint('Tudo certo até o momento.')
print('')

name = winput('Insira o nome da sua distribuição, como definido anteriormente: ')

while not all(validate_character(c) for c in name):
    wprint('Não use letras maiúsculas, números, espaços ou caracteres especiais. Tente novamente.')
    name = winput('Insira um nome para sua distribuição: ')

if not os.path.exists('/mnt/' + name):
    wprint('Diretório /mnt/' + name + ' não encontrado. Talvez você tenha pulado o primeiro script.')
    wprint('Não há como prosseguir. Parando o programa...')
    sys.exit()

if not os.path.ismount('/mnt/' + name):
    wprint('A partição de hospedagem de sua distribuição não está montada.')
    mount_choice = winput('Deseja montá-la agora? (Digite 1 para sim, ou qualquer outro caractere para não)')
    if mount_choice != '1':
        wprint('O script não pode prosseguir. Parando o programa...')
        sys.exit()
    print('')
    mount_partition()

print('')
wprint('O pacote Binutils será compilado.')
ask_to_continue()
compile_host_binutils()

print('')
wprint('O pacote GCC será compilado.')
ask_to_continue()
compile_host_gcc()
