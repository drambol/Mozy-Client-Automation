Feature: Odin Monitoring

  @Prod_monitoring @Odin @syz-mon
  Scenario Outline: Create partner/user group/admin/user/machine then clean up
    Given Use Odin Version <version>
    Then I use odin to query root partner by id
    When I use odin to create new partner with
      | name_prefix |
      | odin_qa_mon_partner_ |
    Then I use odin to query this partner by id
    When I use odin to create new user_group under this partner with
      | name_prefix |
      | odin_qa_mon_user_group_ |
    Then I use odin to query this user_group by id
    When I use odin to create new admin under this partner with
      | full_name_prefix |
      | odin_qa_mon_admin_ |
    Then I use odin to query this admin by id
    When I use odin to deliver email to this admin with
      | email |
      | prod.qa.mon+odinadmin@gmail.com |
    When I use odin to create new user under this user_group with
      | full_name_prefix |
      | odin_qa_mon_user_ |
    Then I use odin to query this user by id
    When I use odin to deliver email to this user with
      | email |
      | prod.qa.mon+odinuser@gmail.com |
    When I use odin to provision resources to this user_group with
      | license_type | licenses |
      | Desktop | 1 |
    When I use odin to create new machine for this user
      | alias_prefix |
      | odin_qa_mon_machine_ |
    Then I use odin to query this machine by id
    Then I use odin to delete this machine by id
    Then I use odin to delete this user by id
    Then I use odin to delete this admin by id
    Then I use odin to delete this user_group by id
    Then I use odin to delete this partner by id

  Examples: Versions
    | version |
    | 0.1.40 |
    | 0.1.42 |
    | 0.1.48 |
    | 0.1.50 |