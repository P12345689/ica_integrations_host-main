# -*- coding: utf-8 -*-
"""LIBICA - IBM Consulting Assistants Extensions API - Python SDK.

Description: Pydantic V2 ICAModel corresponding to the API.

Authors: Mihai Criveti
"""
# pylint: disable=invalid-name

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import (AnyUrl, AwareDatetime, BaseModel, ConfigDict, EmailStr,
                      Field, StringConstraints)
from typing_extensions import Annotated


# INPUT VALIDATION
class GetCatalogUserRolesRequest(BaseModel):
    """
    A Pydantic model for validating input data for used to retrieve a list of user roles for a given catalog instance.

    This class is used to validate that the necessary inputs for the `get_catalog_user_roles` method
    meet the required format and type specifications. It ensures that the email address is valid,
    and that none of the required fields are missing.

    Attributes:
        user_email (EmailStr): A valid email address required for identifying the user.
                                Uses Pydantic's EmailStr for validation to ensure the format is correct.
        team_name (str): The name of the team associated with the user and the security key, should not be empty.
    """

    user_email: EmailStr
    team_name: str


class GetSecurityKeyRequest(BaseModel):
    """
    A Pydantic model for validating input data for retrieving a security key.

    This class is used to validate that the necessary inputs for the `get_security_key` method
    meet the required format and type specifications. It ensures that the email address is valid,
    and that none of the required fields are missing.

    Attributes:
        email_address (EmailStr): A valid email address required for identifying the user.
                                Uses Pydantic's EmailStr for validation to ensure the format is correct.
        team_name (str): The name of the team associated with the user and the security key, should not be empty.
    """

    email_address: EmailStr
    team_name: str


class RemoveSecurityKeyRequest(BaseModel):
    """
    A Pydantic model for validating input data for removing a security key.

    This class is used to validate that the necessary inputs for the `remove_security_key` method
    meet the required format and type specifications. It ensures that the email address is valid,
    and that none of the required fields are missing.

    Attributes:
        email_address (EmailStr): A valid email address required for identifying the user.
                                    Uses Pydantic's EmailStr for validation to ensure the format is correct.
        team_name (str): The name of the team associated with the user and the security key, should not be empty.
    """

    email_address: EmailStr
    team_name: str


# RETURNS
class TeamLabel(BaseModel):
    """
    Represents a label associated with a team.

    This model holds various optional attributes that describe different characteristics of a team label.

    Attributes:
        key (Optional[str]): The key of the label.
        value (Optional[Dict[str, Any]]): The value of the label as a dictionary.
        label (Optional[str]): The actual label text.
        type (Optional[str]): The type of the label, providing additional context.

    Examples:
        >>> team_label = TeamLabel(key="priority", value={"level": "high"}, label="High Priority", type="metadata")
        >>> team_label.key
        'priority'
        >>> team_label.value["level"]
        'high'
        >>> team_label.label
        'High Priority'
    """

    key: Optional[str] = None
    value: Optional[Dict[str, Any]] = None
    label: Optional[str] = None
    type: Optional[str] = None


class PlatformRole(Enum):
    """Enumeration class representing roles in a platform.

    Attributes:
        user (str): Represents a regular user role.
        admin (str): Represents an administrative user role.
        sponsor (str): Represents a sponsor role.
        operator (str): Represents an operator role.
        auditor (str): Represents an auditor role.
        author (str): Represents an author role.
        partner (str): Represents a partner role.
        advisor (str): Represents an advisor role.
    """

    user = "user"
    admin = "admin"
    sponsor = "sponsor"
    operator = "operator"
    auditor = "auditor"
    author = "author"
    partner = "partner"
    advisor = "advisor"


class TeamRole(Enum):
    """
    Enumeration for defining roles within a team.

    These roles determine the permissions and responsibilities assigned to team members.

    Attributes:
        owner (str): Represents the role of a team owner, typically with full administrative rights.
        user (str): Represents a regular team member with standard access rights.

    Examples:
        >>> TeamRole.owner
        <TeamRole.owner: 'owner'>
        >>> TeamRole.user
        <TeamRole.user: 'user'>
    """

    owner = "owner"
    user = "user"


class Status(Enum):
    """
    Enumeration for different status types applicable to objects such as user accounts, tasks, or items in workflows.

    Attributes:
        active (str): Represents an active status, indicating that the object is currently in use or operational.
        inactive (str): Indicates that the object is not currently active but still exists within the system.
        pending_deletion (str): Status indicating that the object is scheduled for deletion.
        deleted (str): Indicates that the object has been removed from the system.
        archived (str): Represents that the object is archived, meaning it is stored away but not active.
        pending_invite (str): Status used for objects that are awaiting a response to an invitation.

    Examples:
        >>> Status.active
        <Status.active: 'active'>
        >>> Status.deleted
        <Status.deleted: 'deleted'>
    """

    active = "active"
    inactive = "inactive"
    pending_deletion = "pending_deletion"
    deleted = "deleted"
    archived = "archived"
    pending_invite = "pending_invite"


class Type(Enum):
    """
    Enumeration representing basic data types that might be used in various applications, from database fields to user input types.

    Attributes:
        text (str): Represents textual data, suitable for storing characters and strings.
        number (str): Represents numerical data, including integers and floating-point numbers.
        boolean (str): Represents boolean data, with possible values of True or False.

    Examples:
        >>> Type.text
        <Type.text: 'text'>
        >>> Type.boolean
        <Type.boolean: 'boolean'>
    """

    text = "text"
    number = "number"
    boolean = "boolean"


class TeamUserAttributes(BaseModel):
    """
    Defines the attributes associated with a team user in an application, providing customization and control over user data fields.

    Attributes:
        key (Optional[str]): The unique identifier for the attribute, used as a reference key.
        label (Optional[str]): A human-readable label for the attribute, used for display purposes.
        type (Optional[Type]): The data type of the attribute, defined by the `Type` enumeration (e.g., text, number, boolean).
        readOnly (Optional[bool]): A flag indicating whether the attribute is read-only, restricting modification post-creation.

    Examples:
        >>> user_attr = TeamUserAttributes(key="role", label="User Role", type=Type.text, readOnly=True)
        >>> user_attr.key
        'role'
        >>> user_attr.readOnly
        True
    """

    key: Optional[str] = None
    label: Optional[str] = None
    type: Optional[Type] = None
    readOnly: Optional[bool] = None


class TeamUserAttributeValue(BaseModel):
    """
    Represents a specific value assigned to a user attribute within a team. This model allows dynamic values to be associated with defined user attributes.

    Attributes:
        key (Optional[str]): The key corresponding to the user attribute for which the value is set.
        value (Optional[Dict[str, Any]]): The value assigned to the attribute, stored as a dictionary that can hold various data types.

    Examples:
        >>> user_attr_value = TeamUserAttributeValue(key="department", value={"name": "Engineering", "floor": 4})
        >>> user_attr_value.key
        'department'
        >>> user_attr_value.value['name']
        'Engineering'
    """

    key: Optional[str] = None
    value: Optional[Dict[str, Any]] = None


class Status1(Enum):
    """
    Enumeration for status options typically used to describe the current state of a catalog instance or similar entity.

    Attributes:
        active (str): Indicates that the entity is active and operational.
        inactive (str): Indicates that the entity is not currently active or operational.

    Examples:
        >>> Status1.active
        <Status1.active: 'active'>
        >>> Status1.inactive
        <Status1.inactive: 'inactive'>
    """

    active = "active"
    inactive = "inactive"


class Type1(Enum):
    """
    Enumeration representing different types of services or assets within a catalog. Useful for categorizing catalog items.

    Attributes:
        service (str): Represents a standard service offering.
        code_asset (str): Represents an asset that is primarily code, such as libraries or scripts.
        global_service (str): Represents services that have a global scope or impact.

    Examples:
        >>> Type1.service
        <Type1.service: 'service'>
        >>> Type1.global_service
        <Type1.global_service: 'global_service'>
    """

    service = "service"
    code_asset = "code_asset"
    global_service = "global_service"


class CatalogInstance(BaseModel):
    """
    Defines a catalog instance within a system, providing detailed information about catalog entries.

    Attributes:
        catalogInstanceId (Optional[str]): Unique identifier for the catalog instance.
        name (Optional[str]): The name of the catalog instance.
        status (Optional[Status1]): The status of the catalog instance, utilizing the `Status1` enumeration.
        displayName (Optional[str]): The display name of the catalog instance, potentially more user-friendly or descriptive.
        catalogId (Optional[str]): Identifier for the catalog this instance belongs to.
        type (Optional[Type1]): The type of catalog instance, categorized by the `Type1` enumeration.

    Examples:
        >>> catalog = CatalogInstance(name="API Services", status=Status1.active, type=Type1.service)
        >>> catalog.name
        'API Services'
        >>> catalog.status
        <Status1.active: 'active'>
    """

    catalogInstanceId: Optional[str] = None
    name: Optional[str] = None
    status: Optional[Status1] = None
    displayName: Optional[str] = None
    catalogId: Optional[str] = None
    type: Optional[Type1] = None


class TeamType(Enum):
    """
    Enumeration representing different types of teams that can be configured within a platform or organization.

    Attributes:
        standard (str): Represents a standard team without specific project or account ties.
        project (str): Represents a team associated specifically with a project.
        account (str): Represents a team associated with a particular account or client.

    Examples:
        >>> TeamType.standard
        <TeamType.standard: 'standard'>
        >>> TeamType.project
        <TeamType.project: 'project'>
    """

    standard = "standard"
    project = "project"
    account = "account"


class TeamMemberList(BaseModel):
    """Represents a list of team members with a maximum of 100 users that can be invited upon team creation.

    Attributes:
        name (Optional[str]): The name of the team member.
        email (Optional[str]): The email address of the team member.
        attributes (Optional[List[TeamUserAttributeValue]]): A list of attributes for the team member.
    """

    name: Optional[str] = None
    email: Optional[str] = None
    attributes: Optional[List[TeamUserAttributeValue]] = None


class TeamMemberAddResult(BaseModel):
    """
    Represents the result of attempting to add a member to a team, encapsulating success or error details.

    Attributes:
        name (Optional[str]): The name of the team member being added.
        email (Optional[str]): The email address of the team member.
        attributes (Optional[List[TeamUserAttributeValue]]): A list of attribute values associated with the team member.
        message (Optional[str]): A message providing additional details about the add operation.
        error (Optional[bool]): A flag indicating whether an error occurred during the add operation.

    Examples:
        >>> result = TeamMemberAddResult(name="John Doe", email="john.doe@example.com", error=False, message="Member added successfully.")
        >>> result.name
        'John Doe'
        >>> result.error
        False
    """

    name: Optional[str] = None
    email: Optional[str] = None
    attributes: Optional[List[TeamUserAttributeValue]] = None
    message: Optional[str] = None
    error: Optional[bool] = None


class Attachment(BaseModel):
    """
    Defines a simple attachment model, typically used to manage file attachments in various applications.

    Attributes:
        id (Optional[str]): The unique identifier for the attachment.
        fileName (Optional[str]): The name of the file attached.

    Examples:
        >>> attachment = Attachment(id="file123", fileName="report.pdf")
        >>> attachment.fileName
        'report.pdf'
    """

    id: Optional[str] = None
    fileName: Optional[str] = None


class Status2(Enum):
    """
    Enumeration for tracking the status of tasks, tickets, or similar items within a system.

    Attributes:
        open (str): Indicates the item is open and requires attention.
        inProgress (str): Indicates work on the item is currently underway.
        resolved (str): Indicates the item has been resolved.
        closed (str): Indicates the item has been closed and no further action is required.
        onHold (str): Indicates the item is on hold, pending further information or action.

    Examples:
        >>> Status2.open
        <Status2.open: 'open'>
        >>> Status2.resolved
        <Status2.resolved: 'resolved'>
    """

    open = "open"
    inProgress = "inProgress"
    resolved = "resolved"
    closed = "closed"
    onHold = "onHold"


class Type2(Enum):
    """
    Enumeration for classifying the type of issue or task in a management system, aiding in sorting and prioritizing.

    Attributes:
        query (str): Represents a general inquiry or request for information.
        issue (str): Represents a problem or bug that needs resolution.
        change (str): Represents a request for changes to be made.
        enhancement (str): Represents a suggestion for improvement or addition.
        deployment (str): Pertains to the deployment of services or software.
        platform (str): Related to issues or tasks specific to the platform infrastructure.
        service (str): Related to services provided by or within the platform.

    Examples:
        >>> Type2.query
        <Type2.query: 'query'>
        >>> Type2.enhancement
        <Type2.enhancement: 'enhancement'>
    """

    query = "query"
    issue = "issue"
    change = "change"
    enhancement = "enhancement"
    deployment = "deployment"
    platform = "platform"
    service = "service"


class SupportTicketRequest(BaseModel):
    """
    Represents a support ticket request within a system.

    This model encapsulates all the necessary details needed to create or manage a support ticket.

    Attributes:
        id (Optional[str]): The unique identifier of the support ticket.
        highLevelGroupId (Optional[str]): The high-level group ID associated with the ticket.
        catalogServiceId (Optional[str]): The catalog service ID related to the ticket.
        createdBy (Optional[str]): The user who created the ticket.
        submittedBy (Optional[str]): The user who submitted the ticket.
        creationDate (Optional[datetime]): The date and time when the ticket was created.
        lastUpdatedDate (Optional[datetime]): The date and time when the ticket was last updated.
        resolutionDate (Optional[datetime]): The date and time when the ticket was resolved.
        resolutionDescription (Optional[str]): A description of the resolution.
        ticketId (Optional[str]): The ticket ID.
        ticketNumber (Optional[str]): The ticket number.
        status (Optional[Status2]): The status of the ticket, mapped to `Status2` enum.
        type (Optional[Type2]): The type of the ticket, mapped to `Type2` enum.
        ticketSummary (Optional[str]): A summary of the ticket.
        ticketDescription (Optional[str]): A detailed description of the ticket.
        attachments (Optional[List[Attachment]]): A list of attachments related to the ticket.
        inProgressDate (Optional[datetime]): The date and time when the ticket status changed to in progress.

    Examples:
        >>> from datetime import datetime
        >>> ticket = SupportTicketRequest(id="1", createdBy="user123", status=Status2.open, type=Type2.query)
        >>> ticket.id
        '1'
        >>> ticket.status
        <Status2.open: 'open'>
    """

    id: Optional[str] = None
    highLevelGroupId: Optional[str] = None
    catalogServiceId: Optional[str] = None
    createdBy: Optional[str] = None
    submittedBy: Optional[str] = None
    creationDate: Optional[AwareDatetime] = None
    lastUpdatedDate: Optional[AwareDatetime] = None
    resolutionDate: Optional[AwareDatetime] = None
    resolutionDescription: Optional[str] = None
    ticketId: Optional[str] = None
    ticketNumber: Optional[str] = None
    status: Optional[Status2] = None
    type: Optional[Type2] = None
    ticketSummary: Optional[str] = None
    ticketDescription: Optional[str] = None
    attachments: Optional[List[Attachment]] = None
    inProgressDate: Optional[AwareDatetime] = None


class IssueAttachment(BaseModel):
    """
    Defines an attachment specifically related to an issue or ticket within a system.

    Attributes:
        attachmentId (Optional[str]): The unique identifier for the issue attachment.
        name (Optional[str]): The name of the file or attachment.

    Examples:
        >>> issue_attachment = IssueAttachment(attachmentId="attach123", name="screenshot.png")
        >>> issue_attachment.name
        'screenshot.png'
    """

    attachmentId: Optional[str] = None
    name: Optional[str] = None


class TicketType(Enum):
    """
    Enumeration of the various types of tickets that can be raised in an issue tracking or support system.

    Attributes:
        query (str): A general inquiry or non-urgent question.
        issue (str): A problem or bug that needs to be addressed.
        change (str): A request for changes to existing systems or configurations.
        enhancement (str): A request for new features or improvements to existing features.
        deployment (str): Related to the deployment of systems or services.
        platform (str): Concerns related to the underlying platform or infrastructure.
        service (str): Issues related to provided services.

    Examples:
        >>> TicketType.issue
        <TicketType.issue: 'issue'>
    """

    query = "query"
    issue = "issue"
    change = "change"
    enhancement = "enhancement"
    deployment = "deployment"
    platform = "platform"
    service = "service"


class Ticket(BaseModel):
    """
    Represents a ticket in a ticketing system, encapsulating all relevant details necessary for managing support or issue resolution processes.

    Attributes:
        id (Optional[str]): Unique identifier for the ticket.
        teamId (Optional[str]): Identifier of the team associated with the ticket.
        teamName (Optional[str]): Name of the team associated with the ticket.
        catalogServiceId (Optional[str]): Identifier of the catalog service related to the ticket.
        catalogServiceName (Optional[str]): Name of the catalog service related to the ticket.
        ticketSummary (Optional[str]): A brief summary of the ticket.
        creationDate (Optional[AwareDatetime]): The date and time the ticket was created.
        lastUpdatedDate (Optional[AwareDatetime]): The date and time the ticket was last updated.
        resolutionDate (Optional[AwareDatetime]): The date and time the ticket was resolved.
        resolutionDescription (Optional[str]): A description of how the ticket was resolved.
        status (Optional[Status2]): The current status of the ticket.
        ticketDescription (Optional[str]): A detailed description of the ticket.
        ticketId (Optional[str]): A secondary identifier for the ticket.
        ticketNumber (Optional[str]): The number assigned to the ticket.
        ticketType (Optional[TicketType]): The type of the ticket.
        attachments (Optional[List[IssueAttachment]]): List of attachments related to the ticket.

    Examples:
        >>> ticket = Ticket(id="1", ticketSummary="Login Issue", status=Status2.open)
        >>> ticket.ticketSummary
        'Login Issue'
        >>> ticket.status
        <Status2.open: 'open'>
    """

    id: Optional[str] = None
    teamId: Optional[str] = None
    teamName: Optional[str] = None
    catalogServiceId: Optional[str] = None
    catalogServiceName: Optional[str] = None
    ticketSummary: Optional[str] = None
    creationDate: Optional[AwareDatetime] = None
    lastUpdatedDate: Optional[AwareDatetime] = None
    resolutionDate: Optional[AwareDatetime] = None
    resolutionDescription: Optional[str] = None
    status: Optional[Status2] = None
    ticketDescription: Optional[str] = None
    ticketId: Optional[str] = None
    ticketNumber: Optional[str] = None
    ticketType: Optional[TicketType] = None
    attachments: Optional[List[IssueAttachment]] = None


class SpecVersion(Enum):
    """
    Enumeration representing the version of the specification used in events, useful in contexts like APIs, where version control is critical.

    Attributes:
        field_0_3 (str): Represents version 0.3 of the specification.
        field_1_0 (str): Represents version 1.0 of the specification.

    Examples:
        >>> SpecVersion.field_0_3
        <SpecVersion.field_0_3: '0.3'>
    """

    field_0_3 = "0.3"
    field_1_0 = "1.0"


class CloudEvent(BaseModel):
    """
    Defines a CloudEvent model for representing events with structured data in cloud-based applications.

    Attributes:
        data (Optional[str]): The payload of the event, typically serialized as a string.
        dataSchema (Optional[AnyUrl]): A URI reference to the schema that describes the data attribute.
        dataContentType (Optional[str]): A content type (MIME type) of the data field.
        subject (Optional[str]): The subject of the event.
        attributeNames (Optional[List[str]]): A list of custom attribute names used within the event.
        id (Optional[str]): A unique identifier for the event.
        type (Optional[str]): The type of the event.
        time (Optional[AwareDatetime]): The timestamp of when the event occurred.
        source (Optional[AnyUrl]): A URI specifying the source of the event.
        specVersion (Optional[SpecVersion]): The specification version used for this event.
        extensionNames (Optional[List[str]]): A list of custom extensions to the event.

    Examples:
        >>> cloud_event = CloudEvent(id="event123", type="user.created", source="https://example.com/source")
        >>> cloud_event.type
        'user.created'
    """

    data: Optional[str] = None
    dataSchema: Optional[AnyUrl] = None
    dataContentType: Optional[str] = None
    subject: Optional[str] = None
    attributeNames: Optional[List[str]] = None
    id: Optional[str] = None
    type: Optional[str] = None
    time: Optional[AwareDatetime] = None
    source: Optional[AnyUrl] = None
    specVersion: Optional[SpecVersion] = None
    extensionNames: Optional[List[str]] = None


class GenericError(BaseModel):
    """
    Represents a generic error response in an application, useful for defining error handling and responses.

    This class is designed to be flexible, allowing for any additional fields as specified by the user.

    Examples:
        # Creating an instance with custom fields
        >>> error = GenericError(code=400, message="Bad Request")
        >>> print(error.json())
        {"code":400,"message":"Bad Request"}

        # Creating an instance with extra fields not predefined in the class
        >>> error = GenericError(code=500, message="Internal Server Error", detail="Unexpected error occurred")
        >>> print(error.json())
        {"code":500,"message":"Internal Server Error","detail":"Unexpected error occurred"}
    """

    model_config = ConfigDict(extra="allow")


class CatalogServicesRolesResponse(BaseModel):
    """
    Represents a response to a request about the roles associated with a specific user for certain services or tools.

    Attributes:
        id (Optional[str]): The unique identifier for the response.
        roleIds (Optional[List[str]]): A list of role identifiers associated with the user.
        userId (Optional[str]): The user identifier for whom roles are being described.
        toolId (Optional[str]): The identifier of the tool or service associated with these roles.

    Examples:
        >>> role_response = CatalogServicesRolesResponse(id="resp123", userId="user456", toolId="tool789")
        >>> role_response.userId
        'user456'
    """

    id: Optional[str] = None
    roleIds: Optional[List[str]] = None
    userId: Optional[str] = None
    toolId: Optional[str] = None


class Type3(Enum):
    """
    Enumeration representing various roles within an organization or system, often used to control access and permissions.

    Attributes:
        user (str): Represents a basic user with standard access.
        admin (str): Represents an administrative user with broad permissions.
        sponsor (str): Typically a stakeholder or financial backer with associated privileges.
        operator (str): Operates critical systems or processes.
        auditor (str): Responsible for auditing and compliance checks.
        author (str): Can create or modify content or code.
        partner (str): An external partner with specific role-based access.
        advisor (str): Provides advice and feedback, often with access to certain information or systems.

    Examples:
        >>> Type3.admin
        <Type3.admin: 'admin'>
    """

    user = "user"
    admin = "admin"
    sponsor = "sponsor"
    operator = "operator"
    auditor = "auditor"
    author = "author"
    partner = "partner"
    advisor = "advisor"


class Status4(Enum):
    """
    Enumeration of possible statuses for entities such as users or tasks, indicating various states they might be in.

    Attributes:
        active (str): The entity is currently active.
        inactive (str): The entity is not currently active.
        pending_deletion (str): The entity is scheduled for deletion.
        deleted (str): The entity has been deleted.
        archived (str): The entity has been archived for preservation.
        pending_invite (str): The entity is awaiting acceptance of an invitation.

    Examples:
        >>> Status4.active
        <Status4.active: 'active'>
        >>> Status4.pending_invite
        <Status4.pending_invite: 'pending_invite'>
    """

    active = "active"
    inactive = "inactive"
    pending_deletion = "pending_deletion"
    deleted = "deleted"
    archived = "archived"
    pending_invite = "pending_invite"


class CreateUserResponse(BaseModel):
    """
    Represents the response received upon creating a user, detailing the new user's account information.

    Attributes:
        id (Optional[str]): The unique identifier of the user.
        email (Optional[str]): The email address of the user.
        name (Optional[str]): The full name of the user.
        type (Optional[Type3]): The role type of the user, based on the `Type3` enumeration.
        status (Optional[Status4]): The current status of the user, according to the `Status4` enumeration.
        isFirstVisit (Optional[bool]): Indicates whether the user has logged in for the first time.
        lastLoginDate (Optional[AwareDatetime]): The date and time of the user's last login.
        firstLoginDate (Optional[AwareDatetime]): The date and time of the user's first login.
        isShowHelp (Optional[bool]): A flag indicating whether help content should be shown to the user.

    Examples:
        >>> new_user = CreateUserResponse(id="user123", email="newuser@example.com", type=Type3.user, status=Status4.active)
        >>> new_user.email
        'newuser@example.com'
        >>> new_user.status
        <Status4.active: 'active'>
    """

    id: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    type: Optional[Type3] = None
    status: Optional[Status4] = None
    isFirstVisit: Optional[bool] = None
    lastLoginDate: Optional[AwareDatetime] = None
    firstLoginDate: Optional[AwareDatetime] = None
    isShowHelp: Optional[bool] = None


class CreateUserRequest(BaseModel):
    """
    Defines the data model for a request to create a new user within a system. This model captures essential user details.

    Attributes:
        email (Optional[str]): The email address of the user to be created.
        name (Optional[str]): The full name of the user.
        firstName (Optional[str]): The first name of the user.
        lastName (Optional[str]): The last name of the user.

    Examples:
        >>> user_request = CreateUserRequest(email="john.doe@example.com", firstName="John", lastName="Doe")
        >>> user_request.firstName
        'John'
    """

    email: Optional[str] = None
    name: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None


class CreateTeamRedirectConfig(BaseModel):
    """
    Represents the configuration settings for redirecting after a team creation process, specifying how certain attributes, categories, and bundles should be handled.

    Attributes:
        attributes (Optional[List[str]]): A list of attribute names to consider during the redirection process.
        categories (Optional[List[str]]): A list of categories relevant to the team that might influence redirection logic.
        bundles (Optional[List[str]]): A list of bundle identifiers that might be assigned or relevant after team creation.

    Examples:
        >>> redirect_config = CreateTeamRedirectConfig(attributes=["priority"], categories=["development"], bundles=["bundle1"])
        >>> redirect_config.categories
        ['development']
    """

    attributes: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    bundles: Optional[List[str]] = None


class CreateTeamRequest(BaseModel):
    """Represents a request to create a new team.

    Attributes:
        name (Annotated[str, StringConstraints(min_length=4, max_length=80)]): The name of the team, which must be unique to the platform and consist only of ASCII alphanumeric and space characters.
        description (Optional[str]): A description of the team.
        owners (List[TeamMemberList]): A list of owners for the team, which must be registered on the platform. At least one owner is required.
        reason (Optional[str]): The reason for creating the team.
        labels (Optional[List[TeamLabel]]): A list of labels associated with the team.
        users (Optional[List[TeamMemberList]]): A list of users to be invited to the team, with a maximum of 100 users upon team creation.
        teamUserAttributes (Optional[List[TeamUserAttributes]]): A list of attributes for team users.
        allowInvitationToPartner (Optional[bool]): Whether to allow invitations to partners.
        redirectConfig (Optional[CreateTeamRedirectConfig]): Configuration for redirection after team creation.
        privateTeam (Optional[bool]): Whether the team is private.

    Note:
        Team name must be unique to platform, consist only of ASCII alphanumeric and space characters.
        owners: Owners must be registered on the platform. At least one owner is required to create a team.
        labels: An instance of the platform may dictate required labels such as Organization. These will be enabled specifically in your platforms Admin > Settings.
        Maximum of 100 users can be invited upon team creation
    """

    name: Annotated[str, StringConstraints(min_length=4, max_length=80)]
    description: Optional[str] = None
    owners: List[TeamMemberList]
    reason: Optional[str] = None
    labels: Optional[List[TeamLabel]] = Field(default=None, title="Team Labels")
    users: Optional[List[TeamMemberList]] = Field(default=None, title="Team Member List")
    teamUserAttributes: Optional[List[TeamUserAttributes]] = Field(default=None, title="Team User Attributes")
    allowInvitationToPartner: Optional[bool] = None
    redirectConfig: Optional[CreateTeamRedirectConfig] = None
    privateTeam: Optional[bool] = None  # Set Private Team setting on new team


class InvitedUser(BaseModel):
    """
    Represents an invited user in a system, detailing their invitation status and relevant personal information.

    Attributes:
        id (Optional[str]): The unique identifier of the invited user.
        name (Optional[str]): The full name of the invited user.
        email (Optional[str]): The email address of the invited user.
        status (Optional[Status4]): The current status of the user's invitation, using the `Status4` enumeration.
        type (Optional[Type3]): The role type assigned to the user, based on the `Type3` enumeration.
        inviteExpirationDate (Optional[AwareDatetime]): The date and time when the invitation will expire.

    Examples:
        >>> invited_user = InvitedUser(id="123", email="invite@example.com", status=Status4.pending_invite)
        >>> invited_user.email
        'invite@example.com'
        >>> invited_user.status
        <Status4.pending_invite: 'pending_invite'>
    """

    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    status: Optional[Status4] = None
    type: Optional[Type3] = None
    inviteExpirationDate: Optional[AwareDatetime] = None


class ErrorDetail(BaseModel):
    """
    Defines the structure for detailing error responses in applications, providing a standardized format for error messaging.

    Attributes:
        code (Optional[int]): A numeric code that represents the specific error type.
        description (Optional[str]): A brief description of the error.
        message (Optional[str]): A more detailed message explaining the error or providing additional context.

    Examples:
        >>> error_detail = ErrorDetail(code=404, description="Not Found", message="The requested resource was not found on the server.")
        >>> error_detail.code
        404
        >>> error_detail.message
        'The requested resource was not found on the server.'
    """

    code: Optional[int] = None
    description: Optional[str] = None
    message: Optional[str] = None


class CreateProjectTeamRequest(BaseModel):
    """
    Defines the data model for a request to create a project team on a platform.

    This model includes all necessary details such as team name, ownership, and additional attributes that support team configuration and management.

    Attributes:
        name (Annotated[str, StringConstraints(min_length=4, max_length=80)]) The name of the team, constrained between 4 and 80 characters, and must be unique within the platform.
        description (Optional[str]): A brief description of the team's purpose and goals.
        owners (List[TeamMemberList]): A list of team members designated as owners, who must be registered on the platform.
        reason (Optional[str]): The reason for creating the team, which might relate to project requirements or organizational needs.
        labels (Optional[List[TeamLabel]]): A list of labels applied to the team, potentially required by platform settings.
        users (Optional[List[TeamMemberList]]): A list of team members to be initially added to the team, with a limit of 100 users upon creation.
        teamUserAttributes (Optional[List[TeamUserAttributes]]): A list of attributes that define additional metadata or settings for team members.
        accountTeamId (str): The identifier of the account team that this project team is associated with, ensuring that the team aligns with existing organizational structures.

    Examples:
        >>> team_request = CreateProjectTeamRequest(
        ...     name="DevOps Squad",
        ...     description="Team focused on improving deployment practices",
        ...     owners=[TeamMemberList(name="Alice Johnson", email="alice@example.com")],
        ...     accountTeamId="acct123"
        ... )
        >>> team_request.name
        'DevOps Squad'
        >>> team_request.accountTeamId
        'acct123'

    Notes:
        name: Team name must be unique to platform, consist only of ASCII alphanumeric and space characters.
        owners: Owners must be registered on the platform. At least one owner is required to create a team.
        labels: An instance of the platform may dictate required labels such as Organization. These will be enabled specifically in your platforms Admin > Settings.
        users: Maximum of 100 users can be invited upon team creation
        accountTeamId: The ID of the account team associated with this project team. Must exist in the platform.
    """

    name: Annotated[str, StringConstraints(min_length=4, max_length=80)]
    description: Optional[str] = None
    owners: List[TeamMemberList]
    reason: Optional[str] = None
    labels: Optional[List[TeamLabel]] = Field(default=None, title="Team Labels")
    users: Optional[List[TeamMemberList]] = Field(default=None, title="Team Member List")
    teamUserAttributes: Optional[List[TeamUserAttributes]] = Field(default=None, title="Team User Attributes")
    accountTeamId: str = Field(..., title="Account Team ID")


class CreateAccountTeamRequest(BaseModel):
    """
    Defines the request parameters for creating an account team within a platform, ensuring that each team has unique identifiers and relevant metadata to manage its operations effectively.

    Attributes:
        name (Annotated[str, StringConstraints(min_length=4, max_length=80)]): The name of the account team, constrained to be between 4 and 80 characters and must be unique on the platform using only ASCII alphanumeric and space characters.
        description (Optional[str]): A brief description of the team's purpose and operations.
        owners (List[TeamMemberList]): A list of team members who have ownership rights on the team.
            All owners must be registered on the platform, and at least one owner is necessary for team creation.
        reason (Optional[str]): The rationale for setting up the team, which could include operational, strategic, or project-specific reasons.
        labels (Optional[List[TeamLabel]]): Labels that may be required or optional, set according to the platform's administration settings, which could include organizational details.
        users (Optional[List[TeamMemberList]]): Specifies the users invited to the team at creation, with a cap at 100 users to maintain manageable team sizes initially.
        teamUserAttributes (Optional[List[TeamUserAttributes]]): Attributes specific to team users that may include roles, permissions, or other metadata.
        organizationId (str): A unique identifier for the organization under which this team is created, ensuring alignment with corporate structure and governance.

    Examples:
        >>> account_team_request = CreateAccountTeamRequest(
        ...     name="Global Research Team",
        ...     description="A team dedicated to coordinating research efforts globally",
        ...     owners=[TeamMemberList(name="Bob Smith", email="bob@example.com")],
        ...     organizationId="org456"
        ... )
        >>> account_team_request.name
        'Global Research Team'
        >>> account_team_request.organizationId
        'org456'

    Notes:
        name: Team name must be unique to platform, consist only of ASCII alphanumeric and space characters.
        owners: Owners must be registered on the platform. At least one owner is required to create a team.
        labels: An instance of the platform may dictate required labels such as Organization. These will be enabled specifically in your platforms Admin > Settings.
        users: Maximum of 100 users can be invited upon team creation
        organizationId: Must be unique across all account teams in the platform.
    """

    name: Annotated[str, StringConstraints(min_length=4, max_length=80)]
    description: Optional[str] = None
    owners: List[TeamMemberList]
    reason: Optional[str] = None
    labels: Optional[List[TeamLabel]] = Field(default=None, title="Team Labels")
    users: Optional[List[TeamMemberList]] = Field(default=None, title="Team Member List")
    teamUserAttributes: Optional[List[TeamUserAttributes]] = Field(default=None, title="Team User Attributes")
    organizationId: str = Field(..., title="Organization ID")


class Author(BaseModel):
    """
    Represents an author.

    Attributes:
        self (Optional[str]): A self.
        key (Optional[str]): A unique key identifying the author in the system.
        accountId (Optional[str]): The system-specific account identifier for the author.
        name (Optional[str]): The full name of the author.
        displayName (Optional[str]): The name of the author as displayed in the system.
        active (Optional[str]): Status indicating whether the author's account is currently active.

    Examples:
        >>> author = Author(name="John Doe", displayName="John D.", active="yes")
        >>> author.displayName
        'John D.'
        >>> author.active
        'yes'
    """

    self: Optional[str] = None
    key: Optional[str] = None
    accountId: Optional[str] = None
    name: Optional[str] = None
    displayName: Optional[str] = None
    active: Optional[str] = None


class Type5(Enum):
    """
    Enumeration defining types of support tickets that can be created, aiding in categorizing and prioritizing issues effectively.

    Attributes:
        query (str): General inquiries or requests for information.
        issue (str): Specific problems or bugs needing resolution.
        change (str): Requests for changes to configurations or setups.
        enhancement (str): Suggestions for improvements or additional features.
        deployment (str): Issues related to the deployment of services or applications.
        platform (str): Concerns specifically related to the platform or underlying infrastructure.
        service (str): Issues directly related to services offered or managed.

    Examples:
        >>> Type5.issue
        <Type5.issue: 'issue'>
        >>> Type5.enhancement
        <Type5.enhancement: 'enhancement'>
    """

    query = "query"
    issue = "issue"
    change = "change"
    enhancement = "enhancement"
    deployment = "deployment"
    platform = "platform"
    service = "service"


class CreateSupportTicketRequest(BaseModel):
    """
    Defines the data model for a request to create a support ticket, which includes necessary details for issue tracking and resolution.

    Attributes:
        ownerId (Optional[str]): The identifier of the owner or creator of the ticket.
        teamId (Optional[str]): The team identifier associated with the ticket, if applicable.
        catalogServiceId (Optional[str]): The catalog service ID related to the ticket.
        subject (Optional[str]): A brief subject or title of the ticket.
        description (Optional[str]): A detailed description of the issue or request.
        type (Optional[Type5]): The type of ticket being created, categorized by the `Type5` enumeration.

    Examples:
        >>> ticket_request = CreateSupportTicketRequest(subject="Login Failure", description="Cannot access dashboard", type=Type5.issue)
        >>> ticket_request.subject
        'Login Failure'
        >>> ticket_request.type
        <Type5.issue: 'issue'>
    """

    ownerId: Optional[str] = None
    teamId: Optional[str] = None
    catalogServiceId: Optional[str] = None
    subject: Optional[str] = None
    description: Optional[str] = None
    type: Optional[Type5] = None


class IssueResponse(BaseModel):
    """
    Represents a response to an issue or ticket request, typically used in systems for tracking bugs, enhancements, or other operational issues.

    Attributes:
        id (Optional[str]): The unique identifier for the issue within the system.
        key (Optional[str]): A system-specific key that may correlate to tracking or project management systems.
        self (Optional[str]): A URL to the resource or issue representation within the system.

    Examples:
        >>> issue_response = IssueResponse(id="12345", key="ISSUE-101")
        >>> issue_response.key
        'ISSUE-101'
        >>> issue_response.id
        '12345'
    """

    id: Optional[str] = None
    key: Optional[str] = None
    self: Optional[str] = None


class SidekickAIGetPromptsRequest(BaseModel):
    """
    Sidekick AI Get Prompts Request.

    Defines the request parameters for retrieving AI-generated prompts based on specified tags and roles.
    This model is used to filter and retrieve prompts that are relevant to specific use cases or user roles.

    Attributes:
        tags (Optional[List[str]]): A list of tags used to categorize and filter prompts.
        roles (Optional[List[str]]): A list of roles to which the prompts are applicable, ensuring relevance to specific user functions.

    Examples:
        >>> get_prompts_request = SidekickAIGetPromptsRequest(tags=["onboarding", "training"], roles=["HR", "trainer"])
        >>> get_prompts_request.tags
        ['onboarding', 'training']
        >>> get_prompts_request.roles
        ['HR', 'trainer']
    """

    tags: Optional[List[str]] = None
    roles: Optional[List[str]] = None


class SidekickAIGetAssistantsRequest(BaseModel):
    """
    Sidekick AI Get Assistants Request.

    Defines the request parameters for retrieving information about available AI assistants based on specified tags and roles.
    This model helps in filtering and selecting assistants that are most suitable for given tasks or user roles.

    Attributes:
        tags (Optional[List[str]]): A list of tags that categorize different assistants according to their capabilities or areas of expertise.
        roles (Optional[List[str]]): A list of roles indicating the suitability of different assistants for specific user groups or functions.

    Examples:
        >>> get_assistants_request = SidekickAIGetAssistantsRequest(tags=["customer support", "data analysis"], roles=["support agent", "data analyst"])
        >>> get_assistants_request.tags
        ['customer support', 'data analysis']
    """

    tags: Optional[List[str]] = None
    roles: Optional[List[str]] = None


class SidekickAIPromptExecutionRequest(BaseModel):
    """
    Sidekick AI Model Execution Request.

    Defines a request for executing a prompt using an AI model, including the necessary parameters to specify the execution context and desired outcomes.

    Attributes:
        prompt (Optional[str]): The prompt text to be executed by the AI.
        systemPrompt (Optional[str]): Additional instructions or context provided to the AI system to guide the execution.
        modelId (Optional[str]): The identifier of the AI model to be used for the execution.
        assistantId (Optional[str]): The identifier of the AI assistant that will handle the prompt.
        collectionId (Optional[str]): The identifier of the collection to which this execution is related.
        documentNames (Optional[List[str]]): Names of documents relevant to the prompt, if applicable.
        chatId (Optional[str]): A chat identifier, if the execution is part of an ongoing conversation.
        parameters (Optional[Dict[str, Dict[str, Any]]]): Detailed parameters for controlling the AI execution, such as thresholds or specific behaviors.
        substitutionParameters (Optional[Dict[str, str]]): Parameters for substituting parts of the prompt with dynamic content.

    Examples:
        >>> prompt_execution_request = SidekickAIPromptExecutionRequest(
        ...     prompt="How do I resolve a login issue?",
        ...     systemPrompt="Provide detailed steps for troubleshooting.",
        ...     modelId="123",
        ...     parameters={"detail_level": {"value": "high"}}
        ... )
        >>> prompt_execution_request.prompt
        'How do I resolve a login issue?'
        >>> prompt_execution_request.parameters["detail_level"]["value"]
        'high'

    Notes:
        modelId: this should be an int.
        assistantId: this should be an int.
        collectionId: this should be a str.
        chatId:this is required.
    """

    prompt: Optional[str] = None
    systemPrompt: Optional[str] = None
    modelId: Optional[str] = None
    assistantId: Optional[str] = None
    collectionId: Optional[str] = None
    documentNames: Optional[List[str]] = None
    chatId: Optional[str] = None
    parameters: Optional[Dict[str, Dict[str, Any]]] = None
    substitutionParameters: Optional[Dict[str, str]] = None


class SidekickAISecurityKeyRequest(BaseModel):
    """
    Sidekick AI Security Key Request.

    Defines a request for generating a security key in the Sidekick AI system, specifying the user's email, associated team, and the key's expiration date.

    Attributes:
        emailAddress (Optional[str]): The email address of the user for whom the security key is being requested.
        teamName (Optional[str]): The name of the team associated with the user, providing context for key usage.
        expiryDate (Optional[AwareDatetime]): The date and time when the security key will expire.

    Examples:
        >>> from datetime import datetime
        >>> from pytz import timezone  # Import pytz library for timezone support
        >>> tz = timezone('UTC')  # Choose the appropriate timezone
        >>> expiry_date = tz.localize(datetime(2024, 12, 31, 23, 59, 59))  # Localize the datetime object to the chosen timezone
        >>> security_key_request = SidekickAISecurityKeyRequest(emailAddress="user@example.com", teamName="Development Team", expiryDate=expiry_date)
        >>> security_key_request.emailAddress
        'user@example.com'
    """

    emailAddress: Optional[str] = None
    teamName: Optional[str] = None
    expiryDate: Optional[AwareDatetime] = None


class SidekickAIPromptRequest(BaseModel):
    """
    Sidekick AI Prompt Request.

    Defines a request for submitting a prompt to Sidekick AI, including necessary details such as the title, description, and expected response.

    Attributes:
        promptTitle (Optional[str]): The title of the prompt, summarizing the essence of the request.
        description (Optional[str]): A detailed description of what the prompt is about or what it aims to achieve.
        prompt (Optional[str]): The actual text of the prompt to be processed by the AI.
        promptResponse (Optional[str]): The expected response or output format from the AI.
        model (Optional[str]): The identifier of the AI model to be used, specifying which model should process the prompt.

    Examples:
        >>> prompt_request = SidekickAIPromptRequest(promptTitle="Ada Lovelace's Biography", description="Biography of Ada Lovelace.", prompt="Provide a short biography of Ada Lovelace", model="222")
        >>> prompt_request.promptTitle
        "Ada Lovelace's Biography"
    """

    promptTitle: Optional[str] = None
    description: Optional[str] = None
    prompt: Optional[str] = None
    promptResponse: Optional[str] = None
    model: Optional[str] = None


class SidekickAICreateChatIdRequest(BaseModel):
    """
    Sidekick AI Chat Id Request.

    Defines a request for creating a chat identifier within the Sidekick AI system, which is used to maintain state or context in ongoing AI-assisted conversations.

    Attributes:
        modelId (Optional[str]): The identifier of the AI model that will be used in the chat.
        assistantId (Optional[str]): The identifier of the AI assistant to be engaged in the chat.
        collectionId (Optional[str]): The identifier of the collection or dataset that the chat may refer to or utilize.

    Examples:
        >>> chat_id_request = SidekickAICreateChatIdRequest(modelId="222")
        >>> chat_id_request.modelId
        '222'

    Note:
        Only one of modelId, assistantId or collectionId is supported.
    """

    modelId: Optional[str] = None
    assistantId: Optional[str] = None
    collectionId: Optional[str] = None


class AuditEventResponse(BaseModel):
    """
    Defines a response for an audit event, indicating whether the event was successfully audited.

    Attributes:
        audited (Optional[bool]): A boolean indicating whether the event was recorded in the audit log.

    Examples:
        >>> audit_response = AuditEventResponse(audited=True)
        >>> audit_response.audited
        True
    """

    audited: Optional[bool] = None


class Role(Enum):
    """
    Enumeration representing roles within a team. These roles determine the level of access and responsibility assigned to team members.

    Attributes:
        owner (str): Indicates the team member has full administrative rights over the team.
        user (str): Indicates the team member has regular access rights.

    Examples:
        >>> Role.owner
        <Role.owner: 'owner'>
    """

    owner = "owner"
    user = "user"


class UpdateTeamMemberRoleRequest(BaseModel):
    """
    Defines a request to update the role of a team member within a system, including their email and new role.

    Attributes:
        email (str): The email address of the team member whose role is being updated. This field must not be blank.
        role (Role): The new role to be assigned to the team member, chosen from the `Role` enumeration.

    Examples:
        >>> update_role_request = UpdateTeamMemberRoleRequest(email="user@example.com", role=Role.owner)
        >>> update_role_request.email
        'user@example.com'
        >>> update_role_request.role
        <Role.owner: 'owner'>

    Notes:
        email: must not be blank
    """

    email: str
    role: Role


class TeamMember1(BaseModel):
    """
    Represents a team member with details including their ID, name, email, and role within the team.

    Attributes:
        id (Optional[str]): The unique identifier of the team member.
        name (Optional[str]): The name of the team member.
        email (Optional[str]): The email address of the team member.
        role (Optional[Role]): The role of the team member within the team, using the `Role` enumeration.

    Examples:
        >>> team_member = TeamMember1(id="123", name="Alice Smith", email="alice@example.com", role=Role.user)
        >>> team_member.name
        'Alice Smith'
        >>> team_member.role
        <Role.user: 'user'>
    """

    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[Role] = None


class UserTeamDetail(BaseModel):
    """
    Details a user's association with a specific team, including the team ID, name, the user's role in that team, and any attributes or labels associated with the team member.

    Attributes:
        teamId (Optional[str]): The unique identifier of the team to which the user belongs.
        teamName (Optional[str]): The name of the team.
        teamRole (Optional[str]): The role of the user within the team.
        attributes (Optional[List[TeamUserAttributeValue]]): A list of attributes specific to the team member.
        teamLabels (Optional[List[TeamLabel]]): A list of labels associated with the team.

    Examples:
        >>> user_detail = UserTeamDetail(teamId="team123", teamName="Dev Team", teamRole="developer")
        >>> user_detail.teamName
        'Dev Team'
        >>> user_detail.teamRole
        'developer'
    """

    teamId: Optional[str] = None
    teamName: Optional[str] = None
    teamRole: Optional[str] = None
    attributes: Optional[List[TeamUserAttributeValue]] = None
    teamLabels: Optional[List[TeamLabel]] = None


class TeamSummary(BaseModel):
    """
    Provides a summary of a team, including its unique identifier, name, type, and any labels associated with it.

    Attributes:
        teamId (Optional[str]): The unique identifier of the team.
        teamName (Optional[str]): The name of the team.
        teamType (Optional[TeamType]): The type of the team, defined by the `TeamType` enumeration.
        labels (Optional[List[TeamLabel]]): A list of labels associated with the team, providing additional context or categorization.

    Examples:
        >>> team_summary = TeamSummary(teamId="team456", teamName="Project Alpha", teamType=TeamType.project)
        >>> team_summary.teamName
        'Project Alpha'
        >>> team_summary.teamType
        <TeamType.project: 'project'>
    """

    teamId: Optional[str] = None
    teamName: Optional[str] = None
    teamType: Optional[TeamType] = None
    labels: Optional[List[TeamLabel]] = None


class Type6(Enum):
    """
    Enumeration representing different types of catalog items or services, useful for categorization within various systems.

    Attributes:
        service (str): Represents a service offering.
        code_asset (str): Represents a code-related asset, such as libraries, scripts, or applications.
        global_service (str): Represents a service offering with global availability or implications.

    Examples:
        >>> Type6.service
        <Type6.service: 'service'>
    """

    service = "service"
    code_asset = "code_asset"
    global_service = "global_service"


class CatalogServiceMember(BaseModel):
    """
    Represents a member of a catalog service, including their user details and the roles they hold within that service.

    Attributes:
        userId (Optional[str]): The unique identifier of the user.
        userName (Optional[str]): The full name of the user.
        userEmail (Optional[str]): The email address of the user.
        roles (Optional[List[str]]): A list of roles the user holds within the catalog service.

    Examples:
        >>> catalog_member = CatalogServiceMember(userId="u123", userName="John Doe", userEmail="johndoe@example.com", roles=["admin", "user"])
        >>> catalog_member.userName
        'John Doe'
    """

    userId: Optional[str] = None
    userName: Optional[str] = None
    userEmail: Optional[str] = None
    roles: Optional[List[str]] = None


class Setting(BaseModel):
    """
    Defines a key-value pair for settings or configurations within various applications.

    Attributes:
        key (Optional[str]): The key or identifier for the setting.
        value (Optional[str]): The value associated with the key.

    Examples:
        >>> setting = Setting(key="theme", value="dark")
        >>> setting.key
        'theme'
    """

    key: Optional[str] = None
    value: Optional[str] = None


class Type7(Enum):
    """
    Enumeration representing types of transitions or statuses that can be assigned during workflows or processes.

    Attributes:
        status (str): Represents a change in status.
        assignee (str): Represents a change in the person assigned to an item.
        chat (str): Represents updates or changes made within a chat context.

    Examples:
        >>> Type7.status
        <Type7.status: 'status'>
    """

    status = "status"
    assignee = "assignee"
    chat = "chat"


class StatusTransition(BaseModel):
    """
    Describes a transition of status within a system, providing details about the change, such as when it happened and who was involved.

    Attributes:
        created (Optional[AwareDatetime]): The timestamp when the transition was created.
        to (Optional[str]): The new status after the transition.
        from_ (Optional[str]): The previous status before the transition, aliased as 'from'.
        name (Optional[str]): The name associated with the transition.
        displayName (Optional[str]): A display-friendly name of the transition.
        type (Optional[Type7]): The type of transition, categorized by the `Type7` enumeration.
        message (Optional[str]): An optional message describing the transition or providing additional context.

    Examples:
        >>> from datetime import datetime
        >>> from pytz import timezone  # Import pytz library for timezone support
        >>> tz = timezone('UTC')  # Choose the appropriate timezone
        >>> created_time = tz.localize(datetime.now())  # Localize the current datetime object to the chosen timezone
        >>> status_change = StatusTransition(created=created_time, to="resolved", from_="open", type=Type7.status, message="Issue resolved")
        >>> status_change.to
        'resolved'
    """

    created: Optional[AwareDatetime] = None
    to: Optional[str] = None
    from_: Optional[str] = Field(default=None, alias="from")
    name: Optional[str] = None
    displayName: Optional[str] = None
    type: Optional[Type7] = None
    message: Optional[str] = None


class Status7(Enum):
    """
    Enumeration representing different status stages for tracking tickets progress or state.

    Attributes:
        open (str): Indicates that the item is open and active.
        inProgress (str): Indicates that work or processes on the item are currently underway.
        resolved (str): Indicates that the issues or tasks associated with the item have been resolved.
        closed (str): Indicates that the item has been closed and no further actions are required.
        onHold (str): Indicates that the item is on hold, awaiting further information or actions.

    Examples:
        >>> Status7.open
        <Status7.open: 'open'>
    """

    open = "open"
    inProgress = "inProgress"
    resolved = "resolved"
    closed = "closed"
    onHold = "onHold"


class TicketDetailResponse(BaseModel):
    """
    Provides a detailed response model for a ticket, encapsulating all pertinent information related to a ticket in a support or issue tracking system.

    Attributes:
        id (Optional[str]): The unique identifier of the ticket.
        teamId (Optional[str]): The identifier of the team associated with the ticket.
        teamName (Optional[str]): The name of the team handling the ticket.
        catalogServiceId (Optional[str]): The identifier of the catalog service related to the ticket.
        catalogServiceName (Optional[str]): The name of the catalog service.
        ticketSummary (Optional[str]): A brief summary of the ticket.
        creationDate (Optional[AwareDatetime]): The date and time when the ticket was created.
        lastUpdatedDate (Optional[AwareDatetime]): The date and time when the ticket was last updated.
        resolutionDate (Optional[AwareDatetime]): The date and time when the ticket was resolved.
        resolutionDescription (Optional[str]): A description of how the ticket was resolved.
        status (Optional[Status7]): The current status of the ticket.
        ticketDescription (Optional[str]): A detailed description of the ticket.
        ticketId (Optional[str]): A secondary identifier for the ticket.
        ticketNumber (Optional[str]): The number assigned to the ticket.
        ticketType (Optional[TicketType]): The type of the ticket.
        attachments (Optional[List[IssueAttachment]]): A list of attachments associated with the ticket.
        history (Optional[List[StatusTransition]]): A history of status transitions for the ticket.
        assignee (Optional[str]): The identifier of the user currently assigned to the ticket.
        owner (Optional[str]): The identifier of the user or team that owns the ticket.
        openBy (Optional[str]): The identifier of the user who originally opened the ticket.

    Examples:
        >>> ticket_response = TicketDetailResponse(
        ...     id="TCK123",
        ...     teamName="IT Support",
        ...     ticketSummary="System Crash on Module X",
        ...     status=Status7.open,
        ...     ticketDescription="The system crashes every time module X is initiated."
        ... )
        >>> ticket_response.teamName
        'IT Support'
        >>> ticket_response.status
        <Status7.open: 'open'>
    """

    id: Optional[str] = None
    teamId: Optional[str] = None
    teamName: Optional[str] = None
    catalogServiceId: Optional[str] = None
    catalogServiceName: Optional[str] = None
    ticketSummary: Optional[str] = None
    creationDate: Optional[AwareDatetime] = None
    lastUpdatedDate: Optional[AwareDatetime] = None
    resolutionDate: Optional[AwareDatetime] = None
    resolutionDescription: Optional[str] = None
    status: Optional[Status7] = None
    ticketDescription: Optional[str] = None
    ticketId: Optional[str] = None
    ticketNumber: Optional[str] = None
    ticketType: Optional[TicketType] = None
    attachments: Optional[List[IssueAttachment]] = None
    history: Optional[List[StatusTransition]] = None
    assignee: Optional[str] = None
    owner: Optional[str] = None
    openBy: Optional[str] = None


class Offering(BaseModel):
    """
    Defines a model for an offering, which typically represents a service or product provided by an organization.

    Attributes:
        name (Optional[str]): The name of the offering.
        url (Optional[str]): The URL where more information about the offering can be found.

    Examples:
        >>> offering = Offering(name="Cloud Storage Service", url="https://example.com/cloud-storage")
        >>> offering.name
        'Cloud Storage Service'
    """

    name: Optional[str] = None
    url: Optional[str] = None


class Type8(Enum):
    """
    Enumeration representing the mandatory or recommended nature of a template or service configuration.

    Attributes:
        Mandatory (str): Indicates that the item or configuration is required.
        Recommended (str): Indicates that the item or configuration is suggested but not required.

    Examples:
        >>> Type8.Mandatory
        <Type8.Mandatory: 'Mandatory'>
    """

    Mandatory = "Mandatory"
    Recommended = "Recommended"


class TemplateSummary(BaseModel):
    """
    Provides a summary of the key features and requirements of a service or product template, used to define its characteristics and conditions of use.

    Attributes:
        requiresVPN (Optional[bool]): Indicates whether using the service requires a VPN.
        isLicensed (Optional[bool]): Specifies if the service is licensed.
        isExternalHosted (Optional[bool]): Indicates if the service is hosted externally.
        isAdminOnly (Optional[bool]): Specifies if only administrators can access or manage the service.
        isThirdParty (Optional[bool]): Indicates if the service is provided by a third party.
        isAssociatedCost (Optional[bool]): Specifies if there are costs associated with the service.
        isAutomatedOnboarding (Optional[bool]): Indicates if the service offers automated onboarding.
        isMultiInstance (Optional[bool]): Specifies if multiple instances of the service can be created.
        isFeaturedService (Optional[bool]): Indicates if the service is featured within the platform.
        isLiteIntegration (Optional[bool]): Specifies if the service offers lite integration options.
        requiresApproval (Optional[bool]): Indicates if using the service requires approval.
        isIBMResearch (Optional[bool]): Specifies if the service is related to IBM Research.
        isRoleInLdap (Optional[bool]): Indicates if the service roles are managed via LDAP.
        isLdapEnabled (Optional[bool]): Specifies if LDAP is enabled for the service.
        isAutoCreateService (Optional[bool]): Indicates if the service can be automatically created.
        autoJoinApproveTool (Optional[bool]): Specifies if the service has a tool for auto-approving join requests.
        isAccountTeamEligible (Optional[bool]): Indicates if the service is eligible for account teams.

    Examples:
        >>> template_summary = TemplateSummary(
        ...     requiresVPN=True, isLicensed=True, isFeaturedService=False,
        ...     isAutomatedOnboarding=True, requiresApproval=False
        ... )
        >>> template_summary.requiresVPN
        True
        >>> template_summary.isFeaturedService
        False
    """

    requiresVPN: Optional[bool] = None
    isLicensed: Optional[bool] = None
    isExternalHosted: Optional[bool] = None
    isAdminOnly: Optional[bool] = None
    isThirdParty: Optional[bool] = None
    isAssociatedCost: Optional[bool] = None
    isAutomatedOnboarding: Optional[bool] = None
    isMultiInstance: Optional[bool] = None
    isFeaturedService: Optional[bool] = None
    isLiteIntegration: Optional[bool] = None
    requiresApproval: Optional[bool] = None
    isIBMResearch: Optional[bool] = None
    isRoleInLdap: Optional[bool] = None
    isLdapEnabled: Optional[bool] = None
    isAutoCreateService: Optional[bool] = None
    autoJoinApproveTool: Optional[bool] = None
    isAccountTeamEligible: Optional[bool] = None


class Type9(Enum):
    """
    Enumeration representing different types of services or assets within a catalog, useful for categorization and identification.

    Attributes:
        service (str): Represents a general service offering.
        code_asset (str): Represents assets primarily consisting of code, such as software libraries or applications.
        global_service (str): Represents services that are available globally across the platform.

    Examples:
        >>> Type9.service
        <Type9.service: 'service'>
    """

    service = "service"
    code_asset = "code_asset"
    global_service = "global_service"


class Industry(Enum):
    """
    Enumeration of various industries, useful for categorizing products, services, or organizational focus within a platform or system.

    Attributes:
        Aerospace_and_Defense (str): Pertains to aerospace and defense industries.
        Automotive (str): Related to the automotive industry.
        Banking___Financial_Markets (str): Concerning banking and financial market sectors.
        Cross_Industry (str): Applicable across multiple industries.
        Education (str): Pertaining to educational institutions and services.
        Electronics (str): Related to the electronics industry.
        Energy_and_Utilities (str): Concerning energy production and utilities.
        Government (str): Related to governmental bodies and services.
        Government___US_Federal (str): Specific to the United States federal government.
        Healthcare (str): Pertaining to the healthcare sector.
        Insurance (str): Related to the insurance industry.
        Life_Sciences (str): Concerning the life sciences sectors.
        Manufacturing (str): Related to manufacturing industries.
        Metals_and_Mining (str): Concerning the metals and mining sectors.
        Oil_and_Gas (str): Related to the oil and gas industry.
        Retail_and_Consumer_Products (str): Pertaining to retail and consumer products.
        Other (str): Other industries not specifically listed.
        Telecommunications__Media_and_Entertainment (str): Related to telecommunications, media, and entertainment sectors.
        Travel_and_Transportation (str): Pertaining to travel and transportation industries.

    Examples:
        >>> Industry.Automotive
        <Industry.Automotive: 'Automotive'>
    """

    Aerospace_and_Defense = "Aerospace and Defense"
    Automotive = "Automotive"
    Banking___Financial_Markets = "Banking & Financial Markets"
    Cross_Industry = "Cross Industry"
    Education = "Education"
    Electronics = "Electronics"
    Energy_and_Utilities = "Energy and Utilities"
    Government = "Government"
    Government___US_Federal = "Government - US Federal"
    Healthcare = "Healthcare"
    Insurance = "Insurance"
    Life_Sciences = "Life Sciences"
    Manufacturing = "Manufacturing"
    Metals_and_Mining = "Metals and Mining"
    Oil_and_Gas = "Oil and Gas"
    Retail_and_Consumer_Products = "Retail and Consumer Products"
    Other = "Other"
    Telecommunications__Media_and_Entertainment = "Telecommunications, Media and Entertainment"
    Travel_and_Transportation = "Travel and Transportation"


class AccessLevel(Enum):
    """
    Enumeration representing different access levels for tools or resources, defining who can access or utilize them.

    Attributes:
        standard (str): Indicates a standard level of access, generally available to most users.
        restricted (str): Indicates restricted access, typically limited to certain users or roles.

    Examples:
        >>> AccessLevel.standard
        <AccessLevel.standard: 'standard'>
    """

    standard = "standard"
    restricted = "restricted"


class ToolTemplateSummary(BaseModel):
    """
    Provides a summary of a tool or template within a platform, detailing its features, usage context, and categorization.

    Attributes:
        id (Optional[str]): The unique identifier of the tool or template.
        name (Optional[str]): The name of the tool or template.
        type (Optional[Type9]): The type of tool or template, as defined by the `Type9` enumeration.
        shortDescription (Optional[str]): A brief description of the tool or template.
        category (Optional[str]): The category under which the tool or template is classified.
        industry (Optional[Industry]): The industry to which the tool or template is related.
        order (Optional[int]): The order or precedence of the tool or template within lists or displays.
        accessLevel (Optional[AccessLevel]): The access level required to utilize the tool or template.
        summary (Optional[TemplateSummary]): A detailed summary of the tool or template's features and requirements.
        description (Optional[str]): A more detailed description of the tool or template.
        documentationUrl (Optional[str]): A URL to the documentation or further information about the tool or template.

    Examples:
        >>> tool_template = ToolTemplateSummary(
        ...     id="12345",
        ...     name="Data Analytics Service",
        ...     type=Type9.service,
        ...     shortDescription="Provides comprehensive data analysis tools.",
        ...     category="Data Management",
        ...     industry=Industry.Telecommunications__Media_and_Entertainment,
        ...     order=1,
        ...     accessLevel=AccessLevel.standard
        ... )
        >>> tool_template.name
        'Data Analytics Service'
        >>> tool_template.industry
        <Industry.Telecommunications__Media_and_Entertainment: 'Telecommunications, Media and Entertainment'>
    """

    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[Type9] = None
    shortDescription: Optional[str] = None
    category: Optional[str] = None
    industry: Optional[Industry] = None
    order: Optional[int] = None
    accessLevel: Optional[AccessLevel] = None
    summary: Optional[TemplateSummary] = None
    description: Optional[str] = None
    documentationUrl: Optional[str] = None


class TeamSetting(BaseModel):
    """Represents a team setting with key and value.

    Represents a key-value pair setting specific to a team, which can be used to customize or configure team-related features or behaviors.

    Attributes:
        key (Optional[str]): The identifier for the setting, which is used to retrieve and modify its value.
        value (Optional[str]): The content or data associated with the key, which dictates the setting's behavior or configuration.

    Examples:
        >>> team_setting = TeamSetting(key="notification_preference", value="email_only")
        >>> team_setting.key
        'notification_preference'
        >>> team_setting.value
        'email_only'

    """

    value: Optional[str] = None
    key: Optional[str] = None


class UserCatalogService(BaseModel):
    """
    Describes a user's association with a specific catalog service, including identification and role details.

    Attributes:
        catalogInstanceId (Optional[str]): The unique identifier for the catalog instance the user is associated with.
        catalogName (Optional[str]): The name of the catalog service.
        roles (Optional[List[str]]): A list of roles that the user holds within this catalog service, defining their permissions and responsibilities.

    Examples:
        >>> user_service = UserCatalogService(catalogInstanceId="123", catalogName="Data Services", roles=["viewer", "editor"])
        >>> user_service.catalogName
        'Data Services'
    """

    catalogInstanceId: Optional[str] = None
    catalogName: Optional[str] = None
    roles: Optional[List[str]] = None


class UserTeam(BaseModel):
    """
    Represents a user's membership in a team, including configurations and associated services.

    Attributes:
        teamId (Optional[str]): The unique identifier for the team.
        teamName (Optional[str]): The name of the team.
        settings (Optional[List[TeamSetting]]): A list of settings specific to this team that can affect various aspects of team functionality.
        catalogServices (Optional[List[UserCatalogService]]): A list of catalog services associated with the team, detailing the user's roles in those services.

    Examples:
        >>> user_team = UserTeam(teamId="team456", teamName="Development Squad", settings=[TeamSetting(key="max_members", value="50")])
        >>> user_team.teamName
        'Development Squad'
        >>> user_team.settings[0].key
        'max_members'
    """

    teamId: Optional[str] = None
    teamName: Optional[str] = None
    settings: Optional[List[TeamSetting]] = None
    catalogServices: Optional[List[UserCatalogService]] = None


class Member(BaseModel):
    """
    Details a member within a system, often used to specify the user's roles and other identifiers in various contexts.

    Attributes:
        userId (Optional[str]): The unique identifier of the member.
        userEmail (Optional[str]): The email address associated with the member.
        roles (Optional[List[str]]): A list of roles that the member holds within the organization or system, defining their access and responsibilities.

    Examples:
        >>> member = Member(userId="user123", userEmail="example@example.com", roles=["admin", "user"])
        >>> member.userEmail
        'example@example.com'
    """

    userId: Optional[str] = None
    userEmail: Optional[str] = None
    roles: Optional[List[str]] = None


class SortObject(BaseModel):
    """
    Defines how objects should be sorted in a query or display, including direction and properties involved in the sorting.

    Attributes:
        direction (Optional[str]): The direction of the sort ('asc' for ascending, 'desc' for descending).
        nullHandling (Optional[str]): How null values should be handled during sorting ('ignore', 'explicit').
        ascending (Optional[bool]): Specifies whether the sort should be in ascending order (True) or descending (False).
        property (Optional[str]): The property of the object on which to sort.
        ignoreCase (Optional[bool]): Whether the sorting should ignore case sensitivity.

    Examples:
        >>> sort_object = SortObject(direction="asc", property="name", ascending=True, ignoreCase=True)
        >>> sort_object.direction
        'asc'
        >>> sort_object.property
        'name'
    """

    direction: Optional[str] = None
    nullHandling: Optional[str] = None
    ascending: Optional[bool] = None
    property: Optional[str] = None
    ignoreCase: Optional[bool] = None


class InputProperty(BaseModel):
    """
    Represents a property with a name and value, typically used for input data in various contexts.

    Attributes:
        name (Optional[str]): The name or identifier of the property.
        value (Optional[str]): The value associated with the property.

    Examples:
        >>> property = InputProperty(name="size", value="large")
        >>> property.name
        'size'
    """

    name: Optional[str] = None
    value: Optional[str] = None


class RequestFormResponse(BaseModel):
    """
    Contains information about a response to a request form, detailing various aspects such as team name, requester details, and purpose.

    Attributes:
        teamName (Optional[str]): The name of the team associated with the request.
        requestCreatedDate (Optional[str]): The date when the request was created.
        requestStatus (Optional[str]): The status of the request.
        requesterName (Optional[str]): The name of the requester.
        requesterEmail (Optional[str]): The email of the requester.
        purpose (Optional[str]): The purpose or reason for the request.
        props (Optional[List[InputProperty]]): A list of input properties associated with the request.

    Examples:
        >>> form_response = RequestFormResponse(teamName="Team A", requestStatus="Pending", requesterName="John Doe")
        >>> form_response.teamName
        'Team A'
    """

    teamName: Optional[str] = None
    requestCreatedDate: Optional[str] = None
    requestStatus: Optional[str] = None
    requesterName: Optional[str] = None
    requesterEmail: Optional[str] = None
    purpose: Optional[str] = None
    props: Optional[List[InputProperty]] = None


class SidekickAIRemoveChatIdRequest(BaseModel):
    """
    Sidekick AI Remove Chat Id Request.

    Request object used for removing a chat ID associated with Sidekick AI.

    Attributes:
        chatId (Optional[str]): The ID of the chat to be removed.

    Examples:
        >>> remove_request = SidekickAIRemoveChatIdRequest(chatId="123")
        >>> remove_request.chatId
        '123'
    """

    chatId: Optional[str] = None


class TeamMember(BaseModel):
    """
    Represents a team member's details, including user information, roles, and attributes.

    Attributes:
        userId (Optional[str]): The unique identifier of the user.
        userName (Optional[str]): The name of the user.
        userEmail (Optional[str]): The email of the user.
        platformRole (Optional[PlatformRole]): The role of the user in the platform.
        teamRole (Optional[TeamRole]): The role of the user within the team.
        status (Optional[Status]): The status of the user.
        joinTeamDate (Optional[AwareDatetime]): The date when the user joined the team.
        lastPlatformVisitDate (Optional[AwareDatetime]): The date of the user's last visit to the platform.
        attributes (Optional[List[TeamUserAttributeValue]]): Additional attributes associated with the user.
        inviteExpirationDate (Optional[AwareDatetime]): The date when the user's invitation expires.

    Examples:
        >>> team_member = TeamMember(userId="user123", userName="Mihai", teamRole=TeamRole.owner)
        >>> team_member.userName
        'Mihai'
    """

    userId: Optional[str] = None
    userName: Optional[str] = None
    userEmail: Optional[str] = None
    platformRole: Optional[PlatformRole] = None
    teamRole: Optional[TeamRole] = None
    status: Optional[Status] = None
    joinTeamDate: Optional[AwareDatetime] = None
    lastPlatformVisitDate: Optional[AwareDatetime] = None
    attributes: Optional[List[TeamUserAttributeValue]] = None
    inviteExpirationDate: Optional[AwareDatetime] = None


class TeamDetailUpdateRequest(BaseModel):
    """
    Update Team Detail Request Object.

    Request object used to update team details, allowing modifications to various aspects such as team name, description, and membership.

    Attributes:
        teamName (Optional[str]): The new name of the team.
        privateTeam (Optional[bool]): Flag indicating whether the team is private or not.
        description (Optional[str]): The new description of the team.
        displayName (Optional[str]): The new display name of the team.
        labels (Optional[List[TeamLabel]]): Updated labels associated with the team.
        members (Optional[List[TeamMember]]): Updated list of team members.
        teamUserAttributes (Optional[List[TeamUserAttributes]]): Updated attributes associated with team members.

    Examples:
        >>> update_request = TeamDetailUpdateRequest(teamName="New Team Name", description="Updated description")
        >>> update_request.teamName
        'New Team Name'
    """

    teamName: Optional[str] = None
    privateTeam: Optional[bool] = None
    description: Optional[str] = None
    displayName: Optional[str] = None
    labels: Optional[List[TeamLabel]] = None
    members: Optional[List[TeamMember]] = None
    teamUserAttributes: Optional[List[TeamUserAttributes]] = None


class TeamDetail(BaseModel):
    """
    Contains detailed information about a team, including its ID, name, type, members, and associated services.

    Attributes:
        teamId (Optional[str]): The unique identifier of the team.
        teamName (Optional[str]): The name of the team.
        displayName (Optional[str]): The display name of the team.
        teamType (Optional[TeamType]): The type of the team.
        labels (Optional[List[TeamLabel]]): The labels associated with the team.
        privateTeam (Optional[bool]): Indicates whether the team is private or not.
        description (Optional[str]): The description of the team.
        logoUrl (Optional[str]): The URL of the team's logo.
        members (Optional[List[TeamMember]]): The list of team members.
        pendingMembers (Optional[List[TeamMember]]): The list of pending team members.
        catalogServices (Optional[List[CatalogInstance]]): The catalog services associated with the team.
        teamUserAttributes (Optional[List[TeamUserAttributes]]): The attributes associated with team members.
        organizationId (Optional[str]): The ID of the organization the team belongs to.
        accountTeamId (Optional[str]): The ID of the account team associated with the team.

    Examples:
        >>> team = TeamDetail(teamName="Team A", description="Description of Team A")
        >>> team.teamName
        'Team A'
    """

    teamId: Optional[str] = None
    teamName: Optional[str] = None
    displayName: Optional[str] = None
    teamType: Optional[TeamType] = None
    labels: Optional[List[TeamLabel]] = None
    privateTeam: Optional[bool] = None
    description: Optional[str] = None
    logoUrl: Optional[str] = None
    members: Optional[List[TeamMember]] = None
    pendingMembers: Optional[List[TeamMember]] = None
    catalogServices: Optional[List[CatalogInstance]] = None
    teamUserAttributes: Optional[List[TeamUserAttributes]] = None
    organizationId: Optional[str] = None
    accountTeamId: Optional[str] = None


class TeamMemberUpdateRequest(BaseModel):
    """
    Join Team Request Object.

    Request object used for updating team membership.

    Attributes:
        users (Optional[List[TeamMemberList]]): The list of team members to be updated.

    Examples:
        >>> update_request = TeamMemberUpdateRequest(users=[TeamMemberList(name="Mihai", role=Role.user)])
        >>> update_request.users[0].name
        'Mihai'
    """

    users: Optional[List[TeamMemberList]] = None


class CreateTeamResponse(BaseModel):
    """
    Response object returned after creating a team, containing details such as the team ID, name, and redirects.

    Attributes:
        id (Optional[str]): The unique identifier of the created team.
        name (Optional[str]): The name of the created team.
        catalogRedirect (Optional[str]): The redirect URL for catalog-related actions.
        launchpadRedirect (Optional[str]): The redirect URL for launchpad-related actions.
        summaryRedirect (Optional[str]): The redirect URL for summary-related actions.
        invitedUsers (Optional[List[InvitedUser]]): The list of invited users to the team.

    Examples:
        >>> create_response = CreateTeamResponse(name="New Team", id="team123")
        >>> create_response.name
        'New Team'
    """

    id: Optional[str] = None
    name: Optional[str] = None
    catalogRedirect: Optional[str] = None
    launchpadRedirect: Optional[str] = None
    summaryRedirect: Optional[str] = None
    invitedUsers: Optional[List[InvitedUser]] = None


class ApiError(BaseModel):
    """
    Represents an error response returned by the API.

    Attributes:
        error (Optional[ErrorDetail]): Details about the error.

    Examples:
        >>> api_error = ApiError(error=ErrorDetail(code=404, description="Resource not found"))
        >>> api_error.error.code
        404
    """

    error: Optional[ErrorDetail] = None


class AddAttachmentResponse(BaseModel):
    """
    Response object returned after adding an attachment, containing details about the attachment.

    Attributes:
        id (Optional[str]): The unique identifier of the attachment.
        self (Optional[str]): The URL of the attachment.
        filename (Optional[str]): The filename of the attachment.
        author (Optional[Author]): Details about the author of the attachment.
        created (Optional[str]): The creation date of the attachment.
        size (Optional[int]): The size of the attachment.
        mimeType (Optional[str]): The MIME type of the attachment.
        content (Optional[str]): The content of the attachment.
        thumbnail (Optional[str]): The URL of the thumbnail image of the attachment.

    Examples:
        >>> attachment_response = AddAttachmentResponse(filename="file.txt", id="attachment123")
        >>> attachment_response.filename
        'file.txt'
    """

    id: Optional[str] = None
    self: Optional[str] = None
    filename: Optional[str] = None
    author: Optional[Author] = None
    created: Optional[str] = None
    size: Optional[int] = None
    mimeType: Optional[str] = None
    content: Optional[str] = None
    thumbnail: Optional[str] = None


class TeamDetail1(BaseModel):
    """
    Contains detailed information about a team, including its ID, name, display name, type, members, and associated IDs.

    Attributes:
        teamId (Optional[str]): The unique identifier of the team.
        teamName (Optional[str]): The name of the team.
        displayName (Optional[str]): The display name of the team.
        teamType (Optional[TeamType]): The type of the team.
        members (Optional[List[TeamMember1]]): The list of team members.
        organizationId (Optional[str]): The ID of the organization the team belongs to.
        accountTeamId (Optional[str]): The ID of the account team associated with the team.

    Examples:
        >>> team_detail = TeamDetail1(teamName="Team A", teamType=TeamType.standard)
        >>> team_detail.teamName
        'Team A'
    """

    teamId: Optional[str] = None
    teamName: Optional[str] = None
    displayName: Optional[str] = None
    teamType: Optional[TeamType] = None
    members: Optional[List[TeamMember1]] = None
    organizationId: Optional[str] = None
    accountTeamId: Optional[str] = None


class UserDetail(BaseModel):
    """
    Contains detailed information about a user, including their ID, name, email address, role, teams, and status.

    Attributes:
        id (Optional[str]): The unique identifier of the user.
        name (Optional[str]): The name of the user.
        emailAddress (Optional[str]): The email address of the user.
        platformRole (Optional[PlatformRole]): The role of the user in the platform.
        teams (Optional[List[UserTeamDetail]]): The teams associated with the user.
        firstLoginDate (Optional[AwareDatetime]): The date of the user's first login.
        lastLoginDate (Optional[AwareDatetime]): The date of the user's last login.
        status (Optional[Status4]): The status of the user.

    Examples:
        >>> user_detail = UserDetail(name="John Doe", emailAddress="john@example.com")
        >>> user_detail.name
        'John Doe'
    """

    id: Optional[str] = None
    name: Optional[str] = None
    emailAddress: Optional[str] = None
    platformRole: Optional[PlatformRole] = None
    teams: Optional[List[UserTeamDetail]] = None
    firstLoginDate: Optional[AwareDatetime] = None
    lastLoginDate: Optional[AwareDatetime] = None
    status: Optional[Status4] = None


class UserSearchResponse(BaseModel):
    """
    Response object returned after searching for users.

    Attributes:
        totalPages (Optional[int]): The total number of pages.
        totalElements (Optional[int]): The total number of elements.
        last (Optional[bool]): Indicates whether it is the last page.
        first (Optional[bool]): Indicates whether it is the first page.
        numberOfElements (Optional[int]): The number of elements in the current page.
        size (Optional[int]): The size of the page.
        number (Optional[int]): The page number.
        users (Optional[List[UserDetail]]): The list of users matching the search criteria.

    Examples:
        >>> search_response = UserSearchResponse(totalPages=5, totalElements=50)
        >>> search_response.totalPages
        5
    """

    totalPages: Optional[int] = None
    totalElements: Optional[int] = None
    last: Optional[bool] = None
    first: Optional[bool] = None
    numberOfElements: Optional[int] = None
    size: Optional[int] = None
    number: Optional[int] = None
    users: Optional[List[UserDetail]] = None


class TeamSearchResponse(BaseModel):
    """
    Response object returned after searching for teams.

    Attributes:
        totalPages (Optional[int]): The total number of pages.
        totalElements (Optional[int]): The total number of elements.
        last (Optional[bool]): Indicates whether it is the last page.
        first (Optional[bool]): Indicates whether it is the first page.
        numberOfElements (Optional[int]): The number of elements in the current page.
        size (Optional[int]): The size of the page.
        number (Optional[int]): The page number.
        records (Optional[List[TeamSummary]]): The list of team summaries matching the search criteria.

    Examples:
        >>> search_response = TeamSearchResponse(totalPages=3, totalElements=30)
        >>> search_response.totalElements
        30
    """

    totalPages: Optional[int] = None
    totalElements: Optional[int] = None
    last: Optional[bool] = None
    first: Optional[bool] = None
    numberOfElements: Optional[int] = None
    size: Optional[int] = None
    number: Optional[int] = None
    records: Optional[List[TeamSummary]] = None


class CatalogDetail(BaseModel):
    """
    Contains detailed information about a catalog, including its name, type, ID, instance URL, settings, and members.

    Attributes:
        catalogName (Optional[str]): The name of the catalog.
        type (Optional[Type6]): The type of the catalog.
        catalogInstanceId (Optional[str]): The unique identifier of the catalog instance.
        catalogId (Optional[str]): The ID of the catalog.
        catalogInstanceUrl (Optional[str]): The URL of the catalog instance.
        settings (Optional[List[Setting]]): The settings of the catalog.
        members (Optional[List[CatalogServiceMember]]): The members of the catalog.

    Examples:
        >>> catalog_info = CatalogDetail(catalogName="Catalog A", type=Type6.service)
        >>> catalog_info.catalogName
        'Catalog A'
    """

    catalogName: Optional[str] = None
    type: Optional[Type6] = None
    catalogInstanceId: Optional[str] = None
    catalogId: Optional[str] = None
    catalogInstanceUrl: Optional[str] = None
    settings: Optional[List[Setting]] = None
    members: Optional[List[CatalogServiceMember]] = None


class RecipeGroup(BaseModel):
    """
    Represents a group of recipes with name, description, tool templates, and order.

    Attributes:
        name (Optional[str]): The name of the recipe group.
        description (Optional[str]): The description of the recipe group.
        toolTemplates (Optional[List[ToolTemplateSummary]]): The tool templates associated with the recipe group.
        order (Optional[int]): The order of the recipe group.

    Examples:
        >>> recipe_group = RecipeGroup(name="Group A", order=1)
        >>> recipe_group.name
        'Group A'
    """

    name: Optional[str] = None
    description: Optional[str] = None
    toolTemplates: Optional[List[ToolTemplateSummary]] = None
    order: Optional[int] = None


class UserCatalogServiceResponse(BaseModel):
    """
    Response object containing user catalog service information.

    Attributes:
        userId (Optional[str]): The unique identifier of the user.
        userName (Optional[str]): The name of the user.
        userEmail (Optional[str]): The email address of the user.
        platformRole (Optional[PlatformRole]): The role of the user in the platform.
        teams (Optional[List[UserTeam]]): The teams associated with the user.

    Examples:
        >>> user_catalog_service = UserCatalogServiceResponse(userId="123", userName="John")
        >>> user_catalog_service.userName
        'John'
    """

    userId: Optional[str] = None
    userName: Optional[str] = None
    userEmail: Optional[str] = None
    platformRole: Optional[PlatformRole] = None
    teams: Optional[List[UserTeam]] = None


class CatalogService(BaseModel):
    """
    Represents a service offered in a catalog with ID and name.

    Attributes:
        catalogInstanceId (Optional[str]): The unique identifier of the catalog instance.
        members (Optional[List[Member]]): The members associated with the catalog service.

    Examples:
        >>> catalog_service = CatalogService(catalogInstanceId="456")
        >>> catalog_service.catalogInstanceId
        '456'
    """

    catalogInstanceId: Optional[str] = None
    members: Optional[List[Member]] = None


class PageableObject(BaseModel):
    """
    Contains pagination information.

    Attributes:
        paged (Optional[bool]): Indicates whether the response is paginated.
        unpaged (Optional[bool]): Indicates whether the response is not paginated.
        pageNumber (Optional[int]): The page number.
        pageSize (Optional[int]): The size of the page.
        offset (Optional[int]): The offset.
        sort (Optional[List[SortObject]]): The sorting information.

    Examples:
        >>> pagination_info = PageableObject(pageNumber=1, pageSize=10)
        >>> pagination_info.pageSize
        10
    """

    paged: Optional[bool] = None
    unpaged: Optional[bool] = None
    pageNumber: Optional[int] = None
    pageSize: Optional[int] = None
    offset: Optional[int] = None
    sort: Optional[List[SortObject]] = None


class Team(BaseModel):
    """
    Contains information about a team, including its ID, name, settings, and catalog services.

    Attributes:
        teamId (Optional[str]): The unique identifier of the team.
        teamName (Optional[str]): The name of the team.
        settings (Optional[List[TeamSetting]]): The settings of the team.
        catalogServices (Optional[List[CatalogService]]): The catalog services associated with the team.

    Examples:
        >>> team_info = Team(teamName="Team A")
        >>> team_info.teamName
        'Team A'
    """

    teamId: Optional[str] = None
    teamName: Optional[str] = None
    settings: Optional[List[TeamSetting]] = None
    catalogServices: Optional[List[CatalogService]] = None


class CatalogRequestFormResponse(BaseModel):
    """
    Response object containing catalog request form information.

    Attributes:
        totalPages (Optional[int]): The total number of pages.
        totalElements (Optional[int]): The total number of elements.
        last (Optional[bool]): Indicates whether it is the last page.
        first (Optional[bool]): Indicates whether it is the first page.
        numberOfElements (Optional[int]): The number of elements.
        size (Optional[int]): The size of the page.
        number (Optional[int]): The page number.
        reportStartDate (Optional[str]): The start date of the report.
        reportEndDate (Optional[str]): The end date of the report.
        templateName (Optional[str]): The name of the template.
        requestForms (Optional[List[RequestFormResponse]]): The request forms.

    Examples:
        >>> catalog_form_response = CatalogRequestFormResponse(templateName="Template A")
        >>> catalog_form_response.templateName
        'Template A'
    """

    totalPages: Optional[int] = None
    totalElements: Optional[int] = None
    last: Optional[bool] = None
    first: Optional[bool] = None
    numberOfElements: Optional[int] = None
    size: Optional[int] = None
    number: Optional[int] = None
    reportStartDate: Optional[str] = None
    reportEndDate: Optional[str] = None
    templateName: Optional[str] = None
    requestForms: Optional[List[RequestFormResponse]] = None


class Recipe(BaseModel):
    """
    Represents a recipe with ID, name, description, category, journey URL, creation date, last updated date, type, owner, offerings, and groups.

    Attributes:
        id (Optional[str]): The unique identifier of the recipe.
        name (Optional[str]): The name of the recipe.
        description (Optional[str]): The description of the recipe.
        category (Optional[str]): The category of the recipe.
        journeyUrl (Optional[str]): The URL of the journey associated with the recipe.
        createdDate (Optional[AwareDatetime]): The creation date of the recipe.
        dateLastUpdated (Optional[AwareDatetime]): The date when the recipe was last updated.
        type (Optional[Type8]): The type of the recipe.
        owner (Optional[str]): The owner of the recipe.
        offerings (Optional[List[Offering]]): The offerings associated with the recipe.
        groups (Optional[List[RecipeGroup]]): The groups associated with the recipe.

    Examples:
        >>> recipe_info = Recipe(name="Recipe A")
        >>> recipe_info.name
        'Recipe A'
    """

    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    journeyUrl: Optional[str] = None
    createdDate: Optional[AwareDatetime] = None
    dateLastUpdated: Optional[AwareDatetime] = None
    type: Optional[Type8] = None
    owner: Optional[str] = None
    offerings: Optional[List[Offering]] = None
    groups: Optional[List[RecipeGroup]] = None


class PageTeam(BaseModel):
    """
    Contains pagination information for teams.

    Attributes:
        totalElements (Optional[int]): The total number of elements.
        totalPages (Optional[int]): The total number of pages.
        numberOfElements (Optional[int]): The number of elements.
        pageable (Optional[PageableObject]): The pagination details.
        size (Optional[int]): The size of the page.
        content (Optional[List[Team]]): The list of teams.
        number (Optional[int]): The page number.
        sort (Optional[List[SortObject]]): The sorting information.
        first (Optional[bool]): Indicates whether it is the first page.
        last (Optional[bool]): Indicates whether it is the last page.
        empty (Optional[bool]): Indicates whether the content is empty.

    Examples:
        >>> page_team_info = PageTeam(totalElements=10)
        >>> page_team_info.totalElements
        10
    """

    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    numberOfElements: Optional[int] = None
    pageable: Optional[PageableObject] = None
    size: Optional[int] = None
    content: Optional[List[Team]] = None
    number: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None
