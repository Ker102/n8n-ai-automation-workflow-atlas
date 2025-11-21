import { repoConfig } from '../config';

const { owner, repo, branch } = repoConfig;

export function getRawDownloadUrl(relativePath) {
  return `https://raw.githubusercontent.com/${owner}/${repo}/${branch}/${relativePath}`;
}

export function getGitHubBlobUrl(relativePath) {
  return `https://github.com/${owner}/${repo}/blob/${branch}/${relativePath}`;
}
