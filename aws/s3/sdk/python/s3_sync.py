"""S3 Directory Sync Tool.

This script syncs files between a local directory and an Amazon S3 bucket
using the AWS CLI's 's3 sync' command.
"""

import argparse
import logging
import os
import subprocess
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

def sync_to_s3(
        local_dir,
        s3_path,
        *,
        delete=False,
        exclude=None,
        include=None,
        dryrun=False,
        quiet=False,
        verbose=False,
        profile=None,
    ) -> bool:
    """Sync local directory to S3 bucket using 'aws s3 sync' command."""
    if not os.path.isdir(local_dir):
        logger.error(f"Local directory does not exist: {local_dir}")
        return False

    # Build the aws s3 sync command
    cmd = ["aws", "s3", "sync", local_dir, s3_path]

    # Add optional flags
    if delete:
        cmd.append("--delete")
    if dryrun:
        cmd.append("--dryrun")
    if quiet:
        cmd.append("--quiet")
    if verbose:
        cmd.append("--verbose")
    if profile:
        cmd.extend(["--profile", profile])

    # Add exclude patterns
    if exclude:
        for pattern in exclude:
            cmd.extend(["--exclude", pattern])

    # Add include patterns
    if include:
        for pattern in include:
            cmd.extend(["--include", pattern])

    logger.info(f"Running command: {' '.join(cmd)}")

    try:
        # Execute the aws s3 sync command
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info("Sync to S3 completed successfully")
        if result.stdout and not quiet:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Sync to S3 failed with code {e.returncode}")
        logger.error(f"Error: {e.stderr}")
        if e.stdout and not quiet:
            print(e.stdout)
        return False

def sync_from_s3(
        s3_path,
        local_dir,
        *,
        delete=False,
        exclude=None,
        include=None,
        dryrun=False,
        quiet=False,
        verbose=False,
        profile=None,
    ) -> bool:
    """Sync S3 bucket to local directory using 'aws s3 sync' command."""
    # Create local directory if it doesn't exist
    os.makedirs(local_dir, exist_ok=True)

    # Build the aws s3 sync command (just swap the order of paths)
    cmd = ["aws", "s3", "sync", s3_path, local_dir]

    # Add optional flags
    if delete:
        cmd.append("--delete")
    if dryrun:
        cmd.append("--dryrun")
    if quiet:
        cmd.append("--quiet")
    if verbose:
        cmd.append("--verbose")
    if profile:
        cmd.extend(["--profile", profile])

    # Add exclude patterns
    if exclude:
        for pattern in exclude:
            cmd.extend(["--exclude", pattern])

    # Add include patterns
    if include:
        for pattern in include:
            cmd.extend(["--include", pattern])

    logger.info(f"Running command: {' '.join(cmd)}")

    try:
        # Execute the aws s3 sync command
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info("Sync from S3 completed successfully")
        if result.stdout and not quiet:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Sync from S3 failed with code {e.returncode}")
        logger.error(f"Error: {e.stderr}")
        if e.stdout and not quiet:
            print(e.stdout)
        return False

def main():
    """Parse arguments and call the sync functions."""
    parser = argparse.ArgumentParser(
        description="Sync files between a local directory and an S3 bucket",
    )
    parser.add_argument("source", help="Source path (local directory or s3://bucket/path)")
    parser.add_argument("destination", help="Destination path (local directory or s3://bucket/path)")
    parser.add_argument("--delete", action="store_true",
                        help="Delete files in destination that don't exist in source")
    parser.add_argument("--exclude", action="append",
                        help="Exclude files/directories that match pattern (can use multiple times)")
    parser.add_argument("--include", action="append",
                        help="Include files/directories that match pattern (can use multiple times)")
    parser.add_argument("--dryrun", action="store_true",
                        help="Display operations that would be performed without actually running them")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress non-error messages")
    parser.add_argument("--verbose", action="store_true",
                        help="Display verbose output")
    parser.add_argument("--profile", help="Use a specific AWS profile from your credentials file")

    args = parser.parse_args()

    # Determine sync direction based on source/destination
    if args.source.startswith("s3://") and not args.destination.startswith("s3://"):
        # S3 to local
        result = sync_from_s3(
            args.source,
            args.destination,
            delete=args.delete,
            exclude=args.exclude,
            include=args.include,
            dryrun=args.dryrun,
            quiet=args.quiet,
            verbose=args.verbose,
            profile=args.profile,
        )
    elif not args.source.startswith("s3://") and args.destination.startswith("s3://"):
        # Local to S3
        result = sync_to_s3(
            args.source,
            args.destination,
            delete=args.delete,
            exclude=args.exclude,
            include=args.include,
            dryrun=args.dryrun,
            quiet=args.quiet,
            verbose=args.verbose,
            profile=args.profile,
        )
    else:
        if args.source.startswith("s3://") and args.destination.startswith("s3://"):
            logger.error("S3 to S3 sync is not supported by this script. Use AWS CLI directly.")
        else:
            logger.error("Invalid source or destination. One must be a local path and the other an S3 path.")
        return 1

    return 0 if result else 1

if __name__ == "__main__":
    sys.exit(main())
