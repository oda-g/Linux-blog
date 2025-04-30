# カーネルビルドメモ

動作環境としては、Ubuntu 24.04 を前提。他のバージョンだと異なっている可能性あり。

## コード取得Ubuntu編

### 最新版取得

「apt source」で取得するのが簡単。

準備:
```
$ sudo vi /etc/apt/sources.list.d/ubuntu.sources  (このファイルを編集する)
Types: deb
URIs: http://jp.archive.ubuntu.com/ubuntu/
Suites: noble noble-updates noble-backports
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

Types: deb
URIs: http://security.ubuntu.com/ubuntu/
Suites: noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

(以下の行を追加。上記をコピーし、Typesをdeb-srcにする。)

Types: deb-src
URIs: http://jp.archive.ubuntu.com/ubuntu/
Suites: noble noble-updates noble-backports
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

Types: deb-src
URIs: http://security.ubuntu.com/ubuntu/
Suites: noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
$
$ sudo apt update
```

コード入手:
```
$ sudo apt build-dep linux  (途中のダイアログでは、noを選択)
$ mkdir build-work  (ビルド用のディレクトリ作成)
$ cd build-work
$ apt source linux (一般ユーザでOK)
```

### 特定の版取得

apt source では必ず最新版になってしまう。特定の版を取得したい場合は以下のとおり。

コードのありか:  
https://launchpad.net/ubuntu/+source/linux/{バージョン}  
ex. https://launchpad.net/ubuntu/+source/linux/6.8.0-52.53/

3つのファイルが存在する。(バージョン部分は適宜読み替え)
- linux_6.8.0.orig.tar.gz
- linux_6.8.0-52.53.diff.gz
- linux_6.8.0-52.53.dsc

それぞれダウンロードし、展開、パッチ適用を行う。以下の手順を行えば、apt source と同等になる。

```
$ mkdir work
$ cd work
$ wget https://launchpad.net/ubuntu/+source/linux/6.8.0-52.53/linux_6.8.0.orig.tar.gz
$ wget https://launchpad.net/ubuntu/+source/linux/6.8.0-52.53/linux_6.8.0-52.53.diff.gz
$ wget https://launchpad.net/ubuntu/+source/linux/6.8.0-52.53/linux_6.8.0-52.53.dsc
$ tar xf linux_6.8.0.orig.tar.gz
$ mv linux-6.8 linux-6.8.0
$ cd linux-6.8.0
$ zcat ../linux_6.8.0-52.53.diff.gz | patch -p1
```

どのバージョンが存在するかは、(どこか既に展開済の)linux-6.8.0/debian/changelog を参照する。

## コンフィグ注意点(Ubuntu編)

Ubuntuのコンフィグでは、Ubuntu特有パッチ内のファイルを参照しているものがある。Ubuntuのコンフィグをベースとし、オリジナルコードをビルドする場合は、それらを修正する必要がある。
```
- CONFIG_SYSTEM_TRUSTED_KEYS="debian/canonical-certs.pem"
- CONFIG_SYSTEM_REVOCATION_KEYS="debian/canonical-revoked-certs.pem"
+ CONFIG_SYSTEM_TRUSTED_KEYS=""
+ CONFIG_SYSTEM_REVOCATION_KEYS=""
```

それぞれ、空文字列にすればOK。(Ubuntuのパッチを当ててビルドする場合は、修正不要)

## 解析準備メモ(Ubuntu編)

Ubuntuのコンフィグをベースにした場合、トレースツール、crash等が使える状態になっている。例えば、debuginfo 付でコンパイルされている。ビルドした環境を維持しておけば、debuginfo パッケージは必要ない。

/lib/modules/{version string}/build にビルドディレクトリへのシンボリックリンクができるので、これを参照すればよい。

- カーネル本体: ex. /lib/modules/6.13.7-test-01/build/vmlinux
- モジュール: ex. /lib/modules/6.13.7-test-01/build/arch/x86/kvm/kvm.ko  
注: インストールされたモジュールの方(/lib/modules/6.13.7-test-01/kernel/arch/x86/kvm/kvm/kvm.ko(or kvm.ko.zst)は、zst圧縮されている場合があるので注意。buildの方を参照しておけば問題ない。

## 起動カーネルの設定

/boot/grub/grub.cfg を確認し、起動したいカーネルのメニュー位置を調べる。ex.

```
$ sudo less /boot/grub/grub.cfg
...
menuentry 'Ubuntu' ... {  ★ 0
        ...
        linux   /vmlinuz-6.8.0-52-generic root=/dev/mapper/ubuntu--vg-ubuntu--lv ro  
        initrd  /initrd.img-6.8.0-52-generic
}
submenu 'Advanced options for Ubuntu' ... {  ★ 1
        menuentry 'Ubuntu, with Linux 6.8.0-52-generic' ... {  ★ 1>0
                ...
                linux   /vmlinuz-6.8.0-52-generic root=/dev/mapper/ubuntu--vg-ubuntu--lv ro  
                echo    'Loading initial ramdisk ...'
                initrd  /initrd.img-6.8.0-52-generic
        }
        menuentry 'Ubuntu, with Linux 6.8.0-52-generic (recovery mode)' ...  {  ★ 1>1
                ...
                linux   /vmlinuz-6.8.0-52-generic root=/dev/mapper/ubuntu--vg-ubuntu--lv ro recovery nomodeset dis_ucode_ldr 
                echo    'Loading initial ramdisk ...'
                initrd  /initrd.img-6.8.0-52-generic
        }
        menuentry 'Ubuntu, with Linux 6.8.0-45-generic' ... {  ★ 1>2
                ...
                linux   /vmlinuz-6.8.0-45-generic root=/dev/mapper/ubuntu--vg-ubuntu--lv ro  
                echo    'Loading initial ramdisk ...'
        }
        ...
```

リブート前に起動カーネルを指定:
```
sudo grub-reboot "1>2" 
sudo reboot
```

恒久的にデフォルトを変えたい場合: /etc/defaut/grub の GRUB_DEFAULT を起動したいものに変更。ex.
```
$ sudo vi /etc/default/grub
GRUB_DEFAULT="1>2" 
...
$
```