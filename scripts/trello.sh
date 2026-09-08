#!/usr/bin/env bash
# Minimal Trello CLI: list lanes, create a ticket, move it between lanes.
# Credentials live in .env (gitignored): TRELLO_KEY, TRELLO_TOKEN, TRELLO_BOARD.
set -euo pipefail

cd "$(dirname "$0")/.."
[ -f .env ] && { set -a; . ./.env; set +a; }
: "${TRELLO_KEY:?add TRELLO_KEY to .env — see .env.example}"
: "${TRELLO_TOKEN:?add TRELLO_TOKEN to .env — see .env.example}"
: "${TRELLO_BOARD:?add TRELLO_BOARD to .env — see .env.example}"

API=https://api.trello.com/1
AUTH=(--data-urlencode "key=$TRELLO_KEY" --data-urlencode "token=$TRELLO_TOKEN")

get()  { curl -fsS --get "$API/$1" "${AUTH[@]}" "${@:2}"; }
post() { curl -fsS -X POST "$API/$1" "${AUTH[@]}" "${@:2}"; }
put()  { curl -fsS -X PUT  "$API/$1" "${AUTH[@]}" "${@:2}"; }

lane_names() { get "boards/$TRELLO_BOARD/lists" --data "fields=name" | jq -r '[.[].name] | join(", ")'; }

lane_id() {
  local id
  id=$(get "boards/$TRELLO_BOARD/lists" --data "fields=name" \
    | jq -r --arg n "$1" 'map(select(.name | ascii_downcase == ($n | ascii_downcase))) | .[0].id // empty')
  [ -n "$id" ] || { echo "no lane named '$1'. Lanes: $(lane_names)" >&2; exit 1; }
  echo "$id"
}

card_id() {
  local matches count
  matches=$(get "boards/$TRELLO_BOARD/cards" --data "fields=name" \
    | jq -c --arg t "$1" 'map(select(.name | startswith($t)))')
  count=$(jq -r 'length' <<<"$matches")
  [ "$count" = 1 ] || { echo "expected 1 card starting with '$1', found $count: $(jq -r '[.[].name] | join(" | ")' <<<"$matches")" >&2; exit 1; }
  jq -r '.[0].id' <<<"$matches"
}

case "${1:-}" in
  lanes)
    lane_names
    ;;
  ls)
    get "boards/$TRELLO_BOARD/lists" --data "cards=open&card_fields=name&fields=name" \
      | jq -r '.[] | "\(.name)", (.cards[]? | "  \(.name)"), ""'
    ;;
  new)
    title=${2:?usage: trello.sh new "AI-005: title" [lane]}
    lane=${3:-$(get "boards/$TRELLO_BOARD/lists" --data "fields=name" | jq -r '.[0].name')}
    post cards --data-urlencode "idList=$(lane_id "$lane")" --data-urlencode "name=$title" \
      | jq -r --arg l "$lane" '"created \(.name) in \($l)"'
    ;;
  move)
    ticket=${2:?usage: trello.sh move AI-005 "In Progress"}
    lane=${3:?usage: trello.sh move AI-005 "In Progress"}
    put "cards/$(card_id "$ticket")" --data-urlencode "idList=$(lane_id "$lane")" \
      | jq -r --arg l "$lane" '"moved \(.name) -> \($l)"'
    ;;
  *)
    echo 'usage: trello.sh lanes | ls | new "AI-005: title" [lane] | move AI-005 "In Progress"' >&2
    exit 2
    ;;
esac
