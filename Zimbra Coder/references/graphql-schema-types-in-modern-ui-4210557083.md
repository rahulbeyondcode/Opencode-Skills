# GraphQL schema types in Modern UI

Source: <https://synacor.atlassian.net/wiki/pages/viewpage.action?pageId=4210557083>

Page ID: 4210557083

Parent ID: 3502866481

Export notes:
- Images and attachments are linked, not downloaded or interpreted.

---

When adding new fields to the GraphQL schema as part of a bug fix or feature development, we need to ensure that the type of the field is always aligned with the backend schema; otherwise, unpredictable behaviours can occur.

Here’s an example: zimbraDataSourceMaxNumEntries was added to the GraphQL schema as a String type when ideally, it should have been an Integer type.

[Image: Screenshot 2025-01-16 at 5.42.28 PM.png](<https://synacor.atlassian.net/wiki/download/attachments/4210557083/Screenshot%202025-01-16%20at%205.42.28%E2%80%AFPM.png>)

The ideal way to get information is if the field type is String/Int/Float then we should refer to LDAP attributes and their type defined in the LDAP attributes list which can be referred to [https://github.com/Zimbra/zm-mailbox/blob/develop/store/conf/attrs/zimbra-attrs.xml#L2239](<https://github.com/Zimbra/zm-mailbox/blob/develop/store/conf/attrs/zimbra-attrs.xml#L2239>)

If the LDAP attribute type says it’s Integer or String, then we should use the same field in GraphQL schema also, if the LDAP attribute type says it’s Long, then in Graphql schema, we need to use Float as type as GraphQL doesn’t support Long type [https://graphql.org/graphql-js/basic-types/](<https://graphql.org/graphql-js/basic-types/>)
