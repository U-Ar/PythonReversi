PYTHONREVERSI -----------------------------------------------------

play.py�̎��s�ɂ��GUI�N���A�R���s���[�^�ƃ��o�[�V�ΐ킪�\
�Ֆʂ̕\���Ƃ��āA�Q�[���ؒT���ɂ̓r�b�g�{�[�h�A
�����̕ۑ��p�ɓ񎟌��z��𗘗p����

�A���t�@�x�[�^�@�ɂ��w�肵���[���܂ŃQ�[���؂�T������
�r�b�g�{�[�h�ł̕]���֐��͌��ݕn��

�Ֆʂ̕ۑ��Đ��@�\�A�҂����@�\�t��


LOG-----------------------------------------------------------------
�F�A�ǂ݂̐[�����w��\�ɂ���
�I�Z���̒ʏ�v���C���\�ɂȂ���
gameboard.previous_step��stringvar�ɒ��O�̎��\��
���ʕ\��������
���z�탂�[�h�̎���
���E�B���h�E��V���ɐ�������o�[�W������test.py�Ƃ��ĊJ���I���A
�ՖʉE�X�y�[�X�̃t���[����UI�Ƃ��ė��p����o�[�W�����𐳎���play.py�Ƃ���
�J���J�n
�����̕ۑ��A�Đ��@�\�̎��� �t�@�C���`��.kif(��q)
--------------------------------------------------------------------


���ݕ�������
�E�]���֐��̃I�v�V�����ύX�@�\���������ABoard.value_func()
�������ւ���̂��K�؂�?
�E�r�b�g���Z�ɂ�鍂�������͂ȕ]���֐��̖�����


�ǉ�����(��]�I�ϑ�)�@�\
�I�v�V�����i���j���[�j����
�v���C���[�T�C�h�̕`����@��I���\�ɂ���
(�����\�����Ȃ��A�ݒu�\�ʒu�̃n�C���C�g�A�]���l�̕\��)


�������ɓ�������
�E�I�u�W�F�N�g�w���ō��Ӗ�����������
�ՖʂɕR�Â���ꂽ�ϐ��ȂǁAGUI�E�B�W�F�b�g���̂��̂ɕR�Â���
�ۑ��������Ƃ��ɂ̓E�B�W�F�b�g�̋@�\���p������������
�ϐ��X���b�g���m�ۂł���̂��֗�������
����ɂ�葼�̊֐�����ł��ϐ����Q�Ƃł���悤�ɂȂ���


################board.py##########################################


class-----Board(b)---------------
�����Ń{�[�h���Ǘ��A�u���ꂽ�΂̗������Ǘ�

���\�b�hreverse,check�Ȃǂō\������A�F�̎w��Ȃ�
�͊O���̃Q�[���Ǘ��Ɉˑ�����

�{�N���X���S������͔̂���Ɛ΂�u�����ۂ̋@�B�I�����Ɗ����̕ۑ�

class variables--------------------------------
self.board
self.reversed_list
self.reversed_record
self.co_record
self.color_record

methods-----------------------------------------

check(self,color,co)
color �F
co �m�F���������W�̃^�v��(x,y)
�Ђ�����Ԃ���E�E�ETrue
�Ԃ��Ȃ��E�E�EFalse


reverse(self,color,co)
�e���ʂ�Ԃ��邩�m�F���������ŕԂ�
���Ԃ��邩�m�F�̕����͂��炩���ߊm�F�������Ă��邽�ߏȗ��\��������Ȃ��̂ŗv����
�Ԃ���������reversed_list�ɋL�^[co1,co2...]
���^�[�����Ƃ�reversed_list��reversed_record�Ɋi�[
�u�������W��co_record�Ɋi�[


undo(self)
reversed_record��co_record�̒��߂��Ƃ���(�j��I)
�Ԃ��ꂽ������Ԃ��Ȃ����A�΂�u�����ʒu��NONE�ɒ���


undo_(self)
�҂����p���\�b�h
undo�Ɨގ��A���O�ɑł������̐F�̕Ԃ�l������


check_gameover(self,color)
�ǂ�������s�s�\�Ɣ��肳�ꂽ�Ƃ�GAMEOVER��Ԃ�
color�̋t���̂ݑ��s�\�Ȏ�PASS��Ԃ�
�ʏ�̎�NORMAL��Ԃ�


put_stone(self,color,co)
reverse�̏��������Q�[�����ɑg�ݍ��ނ��߂ɍœK����������
reverse���s������Acheck_gameover�����s
�Ԃ�l��check_gameover�̒l������


count_stone(self)
�ΐ��̃J�E���g�@�Ԃ�l black,white


print_board(self)
�f�o�b�O�p�R���\�[���\���֐�


value_func(self)
�]���֐�(��)
�ÓI�ȕ]��
�����������炱�����������Ă���
�V���Ȋ֐��Œu��������?


functions-----------------------------------------------------

move_first(depth,b,limit)
move_second(depth,b,limit)
�����̓�����L�q�����֐�
�A���t�@�x�[�^�@�ɂ��depth�Ŏw�肳�ꂽ�[���܂œǂ�


play(first_depth,second_depth)
����AI�Ő�킹��֐�
��Ƀf�o�b�O�p


negamax(color,depth,b,limit)
move_first/second�̈����ɐF��ǉ��A�]���l������Ŕ��]
�����邱�Ƃň�֐��ł̋L�q���\��


play_negamax(first_depth,second_depth)
����negamax�Ő�킹��֐�
��Ƀf�o�b�O�p

co_to_str(co)
���W�ɑ΂��Ċ����p�̕������Ԃ��֐�

##################test.py#######################################
��GUI

�E�B���h�E�ɂ͎��3�`4��ނ�\��
�X�^�[�g���
�I�v�V�������


class---------------------------------------------------------

GameOptionButton(tkinter.Button)(master)
�Q�[���J�n�O�̃I�v�V������ʋN���p�{�^��
command�ϐ��Ɋi�[�\�Ȃ̂��֐��̃|�C���^�݂̂̂��߃��\�b�h��

GameOption(tkinter.Frame)(master)
�I�v�V�������
��/���A�X�e�b�v���A�]���֐��̎�ނ�I��

GameBoardButton(tkinter.Button)(master)
�I�v�V������ʂɕ\������J�n�{�^��
�}�X�^�[�ł���Gameoption����F�A�X�e�b�v���A�]���֐����擾����
boot_gameboard��GameBoard���N������
gameboard_window(Tk())��GameBoard�ƃR���\�[����z�u�A���j���[��
�V�K�Q�[���A�^�C�g����ʁA���f�A���̑��I�v�V������z�u

GameBoard(tkinter.Canvas)(master,color,steps,ai)
�Ֆʂ�`�悷��Ɠ����ɐ΂�u��������Board�N���X�ɓn��
	methods

	put_stone()
	�ՖʂɕR�Â���v���C���[���̊֐�
	�΂�u�������̌��ai_puts_stone�ɓn��

	ai_puts_stone()

	render_board(color)
	�Ֆʕ`��֐�
	����color���v���C���[���̐Fself.color�ƈ�v�����
	�I�v�V�����Ɋ�Â��n�C���C�g�����̎��s(�\��)
	
	undo()
        ���O�̎���Ȃ��������Ƃɂ��Ċ����߂����\�b�h
	�j��I�ł���Arecord��������
	methods��undo�̌�ɕ`�悵�Ȃ����v���C�\�ɂ���

QuitButton(tkinter.Button)(master)
�I���{�^��


----------------.kif----------------------------------
�������ۑ��p�e�L�X�g�t�@�C���`��

#comment                   (#�Ŏn�܂�1�s�ڂ̓R�����g)
20XX/XX/XX XX:XX:XX        (�΋ǊJ�n����)
B black_player
W white_player
XX XX                      (���A���̐ΐ�)
1 B F5                     (�萔 ��� ���W)
2 W F6
....
60 B G2






