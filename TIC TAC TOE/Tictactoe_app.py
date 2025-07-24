import streamlit as st

# Initialize state
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "current_player" not in st.session_state:
    st.session_state.current_player = "X"
if "winner" not in st.session_state:
    st.session_state.winner = None
if "last_clicked" not in st.session_state:
    st.session_state.last_clicked = None

# Reset function
def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.last_clicked = None

# Check for a winner
def check_winner(board):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    for i, j, k in wins:
        if board[i] and board[i] == board[j] == board[k]:
            return board[i]
    if "" not in board:
        return "Draw"
    return None

st.title("🎮 Tic-Tac-Toe")

# Restart button
if st.button("🔄 Restart Game"):
    reset_game()

# Handle move
if st.session_state.last_clicked is not None and st.session_state.winner is None:
    idx = st.session_state.last_clicked
    if st.session_state.board[idx] == "":
        st.session_state.board[idx] = st.session_state.current_player
        st.session_state.winner = check_winner(st.session_state.board)
        if st.session_state.winner is None:
            st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"
    st.session_state.last_clicked = None  # Reset click

# Render board
cols = st.columns(3)
for i in range(3):
    for j in range(3):
        idx = 3*i + j
        with cols[j]:
            if st.session_state.board[idx] == "":
                if st.button(" ", key=f"cell_{idx}"):
                    st.session_state.last_clicked = idx
            else:
                st.markdown(
                    f"<div style='height: 50px; font-size: 28px; text-align: center; border: 1px solid #ccc;'>{st.session_state.board[idx]}</div>",
                    unsafe_allow_html=True
                )

# Game status
if st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.success("🤝 It's a draw!")
    else:
        st.success(f"🎉 Player {st.session_state.winner} wins!")
else:
    st.info(f"🧑 Player {st.session_state.current_player}'s turn")
