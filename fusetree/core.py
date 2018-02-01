import fuse
from fuse import fuse_file_info
from typing import Dict, Iterator, Iterable, Sequence, Tuple, Optional, Any, NamedTuple, Union

import logging
import errno
import time
import threading
import traceback

from . import util
from .types import *

class Node:
    def __getitem__(self, key: str) -> Node_Like:
        return None


    def getattr(self, path: Path) -> Stat_Like:
        """
        Get file attributes.

        Similar to stat().  The 'st_dev' and 'st_blksize' fields are
        ignored. The 'st_ino' field is ignored except if the 'use_ino'
        mount option is given. In that case it is passed to userspace,
        but libfuse and the kernel will still assign a different
        inode for internal use (called the "nodeid").
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def readlink(self, path: Path) -> str:
        """
        Read the target of a symbolic link
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def mknod(self, path: Path, name: str, mode: int, dev: int) -> None:
        """
        Create a file node

        This is called for creation of all non-directory, non-symlink
        nodes.  If the filesystem defines a create() method, then for
        regular files that will be called instead.
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def mkdir(self, path: Path, name: str, mode: int) -> None:
        """
        Create a directory

        Note that the mode argument may not have the type specification
        bits set, i.e. S_ISDIR(mode) can be false.  To obtain the
        correct directory type bits use  mode|S_IFDIR
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def unlink(self, path: Path) -> None:
        """
        Remove a file
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def rmdir(self, path: Path) -> None:
        """
        Remove a directory
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def symlink(self, path: Path, name: str, target: str) -> None:
        """
        Create a symbolic link

        TODO: `target` should probably be a `Path`?
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def rename(self, path: Path, new_path: Path, new_name: str) -> None:
        """
        Rename a file

        FIXME: fuse.h defines an extra `flags` argument
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def link(self, path: Path, name: str, target: Path) -> None:
        """
        Create a hard link to a file
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def chmod(self, path: Path, amode: int) -> None:
        """
        Change the permission bits of a file
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def chown(self, path: Path, uid: int, gid: int) -> None:
        """
        Change the owner and group of a file.
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def truncate(self, path: Path, length: int) -> None:
        """
        Change the size of a file
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def open(self, path: Path, mode: int) -> 'FileHandle':
        """
        File open operation

        No creation (O_CREAT, O_EXCL) and by default also no
        truncation (O_TRUNC) flags will be passed to open(). If an
        application specifies O_TRUNC, fuse first calls truncate()
        and then open(). Only if 'atomic_o_trunc' has been
        specified and kernel version is 2.6.24 or later, O_TRUNC is
        passed on to open.

        Unless the 'default_permissions' mount option is given,
        open should check if the operation is permitted for the
        given flags. Optionally open may also return an arbitrary
        filehandle in the fuse_file_info structure, which will be
        passed to all file operations.
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def setxattr(self, path: Path, name: str, value: bytes, flags: int) -> None:
        """
        Set extended attributes
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def getxattr(self, path: Path, name: str) -> bytes:
        """
        Get extended attributes
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def listxattr(self, path: Path) -> Iterable[str]:
        """
        List extended attributes
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def removexattr(self, path: Path, name: str) -> None:
        """
        Remove extended attributes
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def opendir(self, path: Path) -> DirHandle_Like:

        """
        Open directory

        Unless the 'default_permissions' mount option is given,
        this method should check if opendir is permitted for this
        directory. Optionally opendir may also return an arbitrary
        filehandle in the fuse_file_info structure, which will be
        passed to readdir, closedir and fsyncdir.
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def access(self, path: Path, amode: int) -> int:
        """
        Check file access permissions

        This will be called for the access() system call.  If the
        'default_permissions' mount option is given, this method is not
        called.
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def create(self, path: Path, name: str, mode: int) -> 'FileHandle':
        """
        Check file access permissions

        This will be called for the access() system call.  If the
        'default_permissions' mount option is given, this method is not
        called.
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def utimens(self, path: Path, atime: float, mtime: float) -> None:
        """
        Change the access and modification times of a file with
        nanosecond resolution
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def bmap(self, path: Path, blocksize: int, idx: int) -> int:
        """
        Map block index within file to block index within device

        Note: This makes sense only for block device backed filesystems
        mounted with the 'blkdev' option
        """
        raise fuse.FuseOSError(errno.ENOSYS)


class RootNode(Node):
    def init(self) -> None:
        """
        Initialize filesystem
        """
        pass

    def destroy(self) -> None:
        """
        Clean up filesystem

        Called on filesystem exit.
        """
        pass

    def statfs(self) -> StatVFS:
        """
        Get file system statistics

        The 'f_favail', 'f_fsid' and 'f_flag' fields are ignored
        """
        raise fuse.FuseOSError(errno.ENOSYS)


class DirHandle:
    def __init__(self, node: Node = None) -> None:
        self.node = node

    def readdir(self, path: Path) -> Iterable[DirEntry]:
        """
        Read directory
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def fsyncdir(self, path: Path, datasync: int) -> None:
        """
        Synchronize directory contents

        If the datasync parameter is non-zero, then only the user data
        should be flushed, not the meta data
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def releasedir(self, path: Path) -> None:
        """
        Release directory
        """
        pass



class FileHandle:
    def __init__(self, node: Node = None, direct_io: bool = False) -> None:
        self.node = node
        self.direct_io = direct_io

    def getattr(self, path: Path) -> Stat_Like:
        """
        Get file attributes of an open file.

        Similar to stat().  The 'st_dev' and 'st_blksize' fields are
        ignored. The 'st_ino' field is ignored except if the 'use_ino'
        mount option is given. In that case it is passed to userspace,
        but libfuse and the kernel will still assign a different
        inode for internal use (called the "nodeid").
        """
        return self.node.getattr(path)

    def chmod(self, path: Path, amode: int) -> None:
        """
        Change the permission bits of an open file.

        FIXME: This doesn't seem to be supported by fusepy
        """
        return self.node.chmod(path, amode)

    def chown(self, path: Path, uid: int, gid: int) -> None:
        """
        Change the owner and group of an open file.

        FIXME: This doesn't seem to be supported by fusepy
        """
        return self.node.chown(path, uid, gid)

    def truncate(self, path: Path, length: int) -> None:
        """
        Change the size of a file
        """
        return self.node.truncate(path, length)

    def read(self, path: Path, size: int, offset: int) -> bytes:
        """
        Read data from an open file

        Read should return exactly the number of bytes requested except
        on EOF or error, otherwise the rest of the data will be
        substituted with zeroes.	 An exception to this is when the
        'direct_io' mount option is specified, in which case the return
        value of the read system call will reflect the return value of
        this operation.
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def write(self, path: Path, data: bytes, offset: int) -> int:
        """
        Write data to an open file

        Write should return exactly the number of bytes requested
        except on error. An exception to this is when the 'direct_io'
        mount option is specified (see read operation).
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def flush(self, path: Path) -> None:
        """
        Possibly flush cached data

        BIG NOTE: This is not equivalent to fsync().  It's not a
        request to sync dirty data.

        Flush is called on each close() of a file descriptor.  So if a
        filesystem wants to return write errors in close() and the file
        has cached dirty data, this is a good place to write back data
        and return any errors.  Since many applications ignore close()
        errors this is not always useful.

        NOTE: The flush() method may be called more than once for each
        open().	This happens if more than one file descriptor refers
        to an opened file due to dup(), dup2() or fork() calls.	It is
        not possible to determine if a flush is final, so each flush
        should be treated equally.  Multiple write-flush sequences are
        relatively rare, so this shouldn't be a problem.

        Filesystems shouldn't assume that flush will always be called
        after some writes, or that if will be called at all.
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def release(self, path: Path) -> None:
        """
        Release an open file

        Release is called when there are no more references to an open
        file: all file descriptors are closed and all memory mappings
        are unmapped.

        For every open() call there will be exactly one release() call
        with the same flags and file descriptor.	 It is possible to
        have a file opened more than once, in which case only the last
        release will mean, that no more reads/writes will happen on the
        file.  The return value of release is ignored.
        """
        pass

    def fsync(self, path: Path, datasync: int) -> None:
        """
        Release an open file

        Release is called when there are no more references to an open
        file: all file descriptors are closed and all memory mappings
        are unmapped.

        For every open() call there will be exactly one release() call
        with the same flags and file descriptor.	 It is possible to
        have a file opened more than once, in which case only the last
        release will mean, that no more reads/writes will happen on the
        file.  The return value of release is ignored.
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def lock(self, path: Path, cmd: int, lock: Any) -> None:
        """
        Perform POSIX file locking operation

        The cmd argument will be either F_GETLK, F_SETLK or F_SETLKW.

        For the meaning of fields in 'struct flock' see the man page
        for fcntl(2).  The l_whence field will always be set to
        SEEK_SET.

        For checking lock ownership, the 'fuse_file_info->owner'
        argument must be used.

        For F_GETLK operation, the library will first check currently
        held locks, and if a conflicting lock is found it will return
        information without calling this method.	 This ensures, that
        for local locks the l_pid field is correctly filled in.	The
        results may not be accurate in case of race conditions and in
        the presence of hard links, but it's unlikely that an
        application would rely on accurate GETLK results in these
        cases.  If a conflicting lock is not found, this method will be
        called, and the filesystem may fill out l_pid by a meaningful
        value, or it may leave this field zero.

        For F_SETLK and F_SETLKW the l_pid field will be set to the pid
        of the process performing the locking operation.

        Note: if this method is not implemented, the kernel will still
        allow file locking to work locally.  Hence it is only
        interesting for network filesystems and similar.

        FIXME: fusepy doesn't seem to support it properly
        """
        raise fuse.FuseOSError(errno.ENOSYS)

    def utimens(self, path: Path, atime: float, mtime: float) -> None:
        """
        Change the access and modification times of a file with
        nanosecond resolution
        """
        return self.node.utimens(path, atime, mtime)
