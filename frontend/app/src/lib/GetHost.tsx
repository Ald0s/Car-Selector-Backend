/**
 * Return the server toward which we should direct API queries.
 * 
 * @returns The hostname/domain for the current server.
 */
export default function getHost() {
  return window.location.origin;
}
