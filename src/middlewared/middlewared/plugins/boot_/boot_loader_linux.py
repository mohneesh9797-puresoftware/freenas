import os
import shutil
import tempfile

from middlewared.service import private, Service
from middlewared.utils import run

from .boot_loader_base import BootLoaderBase


class BootService(Service, BootLoaderBase):

    @private
    async def install_loader(self, dev):
        await run('grub-install', '--target=i386-pc', f'/dev/{dev}')
        await run('mkdosfs', '-F', '32', '-s', '1', '-n', 'EFI', f'/dev/{dev}2')
        with tempfile.TemporaryDirectory() as tmpdirname:
            efi_dir = os.path.join(tmpdirname, 'efi')
            os.makedirs(efi_dir)
            await run('mount', '-t', 'vfat', f'/dev/{dev}2', efi_dir)
            await run(
                'grub-install', '--target=x86_64-efi', f'--efi-directory={efi_dir}',
                '--bootloader-id=debian', '--recheck', '--no-floppy',
            )
            mounted_efi_dir = os.path.join(efi_dir, 'EFI')
            os.makedirs(os.path.join(mounted_efi_dir, 'boot'), exist_ok=True)
            shutil.copy(
                os.path.join(mounted_efi_dir, 'debian/grubx64.efi'),
                os.path.join(mounted_efi_dir, 'boot/bootx64.efi')
            )
            await run('umount', efi_dir)
