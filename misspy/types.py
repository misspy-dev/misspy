from __future__ import annotations
from typing import Any

class poll:
    def __init__(
        self,
        choices: list,
        multiple: bool = False,
        expiresAt: int = None,
        expiredAfter: int = None,
    ):
        self.choices = choices
        self.multiple = multiple
        self.expiresAt = expiresAt
        self.expiredAfter = expiredAfter

class Note:
    
    def __init__(
        self,
        id: str,
        createdAt: str,
        text: str,
        cw: str,
        user: User,
        userId: str,
        visibility: str
    ) -> None:
        self.id = id
        self.createdAt = createdAt
        self.text = text
        self.cw = cw
        self.user = user
        self.userId = userId
        self.visibility = visibility

class User:
    
    def __init__(
        self,
        id: str,
        createdAt: str,
        username: str,
        host: str,
        name: str,
        onlineStatus: str,
        avatarUrl: str,
        avatarBlurhash: str
    ) -> None:
        self.id = id
        self.createdAt = createdAt
        self.username = username
        self.host = host
        self.name = name
        self.onlineStatus = onlineStatus
        self.avatarUrl = avatarUrl
        self.avatarBlurhash = avatarBlurhash

class Drive:
    
    def __init__(
        self,
        capacity: int,
        usage: int
    ) -> None:
        self.capacity = capacity
        self.usage = usage
        
class MyProfile:
    """
    This is a type unique to misspy.
    """
    
    def __init__(
        self,
        id: str,
        name: str,
        username: str,
        avatarUrl: str,
        avatarBlurhash,
        avatarDecorations: list,
        isBot: bool,
        isCat: bool,
        emojis,
        onlineStatus: str,
        badgeRoles: list,
        followersCount: int,
        followingCount: int,
        achievements,
        loggedInDays,
        policies,
        fields: list=[],
        verifiedLinks: list=[],
        pinnedNoteIds: list=[],
        pinnedNotes: list=[],
        pinnedPageId=None,
        pinnedPage=None, 
        publicReactions=True,
        ffVisibility="public",
        twoFactorEnabled=False,
        usePasswordLessLogin=False,
        securityKeys=False,
        roles: list=[],
        memo=None,
        avatarId=None,
        bannerId=None,
        isModerator=False,
        isAdmin=False,
        injectFeaturedNote=True,
        receiveAnnouncementEmail=True,
        alwaysMarkNsfw=False,
        autoSensitive=False,
        carefulBot=False,
        autoAcceptFollowed=True, 
        noCrawle=False,
        preventAiLearning=True,
        isExplorable=True,
        isDeleted=False,
        twoFactorBackupCodesStock="none",
        hideOnlineStatus=False,
        hasUnreadSpecifiedNotes=False,
        hasUnreadMentions=False,
        hasUnreadAnnouncement=False, 
        unreadAnnouncements=[],
        hasUnreadAntenna=False,
        hasUnreadChannel=False,
        hasUnreadNotification=False,
        hasPendingReceivedFollowRequest=False,
        unreadNotificationsCount=0,
        mutedWords=[], 
        mutedInstances=[],
        mutingNotificationTypes=[],
        notificationRecieveConfig={},
        emailNotificationTypes=[
            "follow",
            "receiveFollowRequest"
        ],
        email=None,
        emailVerified=False,
        securityKeysList=[],
        url: str=None,
        uri: str=None,
        movedTo=None, 
        alsoKnownAs=None,
        updatedAt=None,
        lastFetchedAt=None,
        bannerUrl=None,
        bannerBlurhash=None,
        isLocked=None,
        isSilenced=None,
        isSuspended=None, 
        description=None,
        location=None,
        birthday=None,
        lang=None,
        host=None
    ) -> None:
        self.id = id
        self.name = name
        self.username = username
        self.host = host
        self.avatarUrl = avatarUrl
        self.avatarBlurhash = avatarBlurhash
        self.avatarDecorations = avatarDecorations
        self.isBot = isBot
        self.isCat = isCat
        self.emojis = emojis
        self.onlineStatus = onlineStatus
        self.badgeRoles = badgeRoles
        self.followersCount = followersCount
        self.followingCount = followingCount
        self.achievements = achievements
        self.loggedInDays = loggedInDays
        self.policies = policies
        self.fields = fields
        self.verifiedLinks = verifiedLinks
        self.pinnedNoteIds = pinnedNoteIds
        self.pinnedNotes = pinnedNotes
        self.pinnedPageId = pinnedPageId
        self.pinnedPage = pinnedPage
        self.publicReactions = publicReactions 
        self.ffVisibility = ffVisibility
        self.twoFactorEnabled = twoFactorEnabled
        self.usePasswordLessLogin = usePasswordLessLogin
        self.securityKeys = securityKeys
        self.roles = roles
        self.memo = memo
        self.avatarId = avatarId
        self.bannerId = bannerId
        self.isModerator = isModerator
        self.isAdmin = isAdmin
        self.injectFeaturedNote = injectFeaturedNote
        self.receiveAnnouncementEmail = receiveAnnouncementEmail
        self.alwaysMarkNsfw = alwaysMarkNsfw
        self.autoSensitive = autoSensitive
        self.carefulBot = carefulBot
        self.autoAcceptFollowed = autoAcceptFollowed
        self.noCrawle = noCrawle
        self.preventAiLearning = preventAiLearning
        self.isExplorable = isExplorable
        self.isDeleted = isDeleted
        self.twoFactorBackupCodesStock = twoFactorBackupCodesStock
        self.hideOnlineStatus = hideOnlineStatus
        self.hasUnreadSpecifiedNotes = hasUnreadSpecifiedNotes
        self.hasUnreadMentions = hasUnreadMentions
        self.hasUnreadAnnouncement = hasUnreadAnnouncement
        self.unreadAnnouncements = unreadAnnouncements
        self.hasUnreadAntenna = hasUnreadAntenna
        self.hasUnreadChannel = hasUnreadChannel
        self.hasUnreadNotification = hasUnreadNotification
        self.hasPendingReceivedFollowRequest = hasPendingReceivedFollowRequest
        self.unreadNotificationsCount = unreadNotificationsCount
        self.mutedWords = mutedWords
        self.mutedInstances = mutedInstances
        self.mutingNotificationTypes = mutingNotificationTypes
        self.notificationRecieveConfig = notificationRecieveConfig
        self.emailNotificationTypes = emailNotificationTypes
        self.email = email
        self.emailVerified = emailVerified
        self.securityKeysList = securityKeysList
        self.url = url
        self.uri = uri
        self.movedTo = movedTo 
        self.alsoKnownAs = alsoKnownAs 
        self.updatedAt = updatedAt 
        self.lastFetchedAt = lastFetchedAt 
        self.bannerUrl = bannerUrl 
        self.bannerBlurhash = bannerBlurhash 
        self.isLocked = isLocked 
        self.isSilenced = isSilenced
        self.isSuspended = isSuspended
        self.description = description
        self.location = location
        self.birthday = birthday
        self.lang = lang
        self.host = host