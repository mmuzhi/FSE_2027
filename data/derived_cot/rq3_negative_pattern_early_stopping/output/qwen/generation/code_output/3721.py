class Solution:
    def countMentions(self, numberOfUsers: int, events: List[List[str]]) -> List[int]:
        # Sort events by timestamp (converted to int) and then by type (OFFLINE first)
        events.sort(key=lambda x: (int(x[1]), 0 if x[0]=='OFFLINE' else 1))
        
        mentions = [0] * numberOfUsers
        last_offline = [-1] * numberOfUsers
        
        for event in events:
            timestamp = int(event[1])
            if event[0] == "OFFLINE":
                # Extract user id from the third element
                user_id = int(event[2].split('id')[1])
                last_offline[user_id] = timestamp
            else:  # MESSAGE event
                # Parse the mentions_string
                tokens = event[2].split()
                for token in tokens:
                    if token == "ALL":
                        for uid in range(numberOfUsers):
                            mentions[uid] += 1
                    elif token == "HERE":
                        for uid in range(numberOfUsers):
                            if last_offline[uid] == -1 or last_offline[uid] + 60 <= timestamp:
                                mentions[uid] += 1
                    else:
                        # It's an id token
                        # Extract the user id from the token (starts with "id")
                        # The token is "id<number>", so we take the part after "id"
                        user_id = int(token[2:])
                        mentions[user_id] += 1
        
        return mentions