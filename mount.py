import os
import os.path
import sys
import csv
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


def check_linux_id():
    release_info = {}
    if os.path.exists('/etc/os-release'):
        with open('/etc/os-release') as os_release:
            reading = csv.reader(os_release, delimiter = "=")
            for row in reading:
                if row:
                    release_info[row[0]] = row[1]
    else:
        wprint('ERRO: Arquivo /etc/os-release inexistente ou inacessível.')
        sys.exit()
    if release_info['ID'] in ['ubuntu', 'linuxmint', 'fedora']:
        return release_info['ID']
    else:
        wprint('ERRO: Distribuição não suportada.')
        sys.exit()


def check_partition_availability():
    if os.path.exists('/mnt/' + name):
        if os.path.ismount('/mnt/' + name):
            wprint('ERRO: Já há um volume montado em /mnt/' + name + '.')
            sys.exit()


def validate_character(character):
    if character in 'qwertyuiopasdfghjklzxcvbnm':
        return True
    else:
        return False


def mount_partition():
    partition = winput('Insira a partição onde sua distribuição está hospedada (ex: sda5 ou sdb1): ')
    while not os.path.exists('/dev/' + partition):
        wprint('Essa partição não existe no sistema hospedeiro. Tente novamente.')
        partition = winput('Insira uma partição para hospedar sua distribuição (ex: sda5 ou sdb1): ')
    os.system('mount -v -t ext4 /dev/' + partition + ' /mnt/' + name)


os.system('clear')

print('')
wprint('[Linux Distribution Builder]')
print('')
wprint('Este script pretende criar uma distribuição Linux, baseando-se no livro Linux From Scratch 10.0. Acesse o material em http://www.linuxfromscratch.org/ para ter uma noção mais aprofundada do que vem adiante.')
print('')
wprint('Script em execução: script de montagem.')
print('')
wprint('O que este script fará neste sistema (sistema hospedeiro):')
wprint(' - Montará a partição de hospedagem em /mnt/<<<nome da distribuição>>>;')

ask_to_continue()

wprint('Verificando requisitos de execução...')
check_architecture()
check_system()
check_linux_id()
check_user()
wprint('Tudo certo até o momento.')
print('')

name = winput('Insira um nome para sua distribuição: ')

while not all(validate_character(c) for c in name):
    wprint('Não use letras maiúsculas, números, espaços ou caracteres especiais.')
    name = winput('Insira um nome para sua distribuição: ')

print('')
wprint('Verificando requisitos de execução...')
check_partition_availability()
wprint('Tudo certo até o momento.')

print('')
mount_partition()

print('')
wprint('Pronto!')
print('')
