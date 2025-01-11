# import pytest
#
# from cvx.cradle.cli import cli
#
#
# def test_experiments(templates_dir, tmp_path):
#     with pytest.raises(RuntimeError):
#         cli(
#             template=str(templates_dir / "experiments"),
#             context={"GitHub Username": "Peter Maffay",
#                      "Project Name": "test",
#                      "Visibility": "public",
#                      "Description": "",
#                      "Repository URL":"",
#                      "SSH URI": "",
#                      "Command to create the repo":""
#                      }
#         )
#
#
# def test_paper(templates_dir, tmp_path):
#     with pytest.raises(RuntimeError):
#         cli(
#             template=str(templates_dir / "paper"),
#             user_defaults={"username": "Peter Maffay", "project_name": "test"},
#         )
#
#
# def test_pack(templates_dir, tmp_path):
#     with pytest.raises(RuntimeError):
#         cli(
#             template=str(templates_dir / "package"),
#             user_defaults={"username": "Peter Maffay", "project_name": "test"},
#         )
